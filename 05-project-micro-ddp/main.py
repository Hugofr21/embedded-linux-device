import os
import torch
import torch.nn as nn
import torch.distributed as dist
import torch.multiprocessing as mp
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler

# Importações dos módulos criados anteriormente
from src.model import LinearPredictor
from src.engine import MicroDDPOrchestrator

def preparar_dados_reais(rank: int, world_size: int):
    """
    Carrega, normaliza e particiona o dataset empirico de acordo com o Rank.
    """
    # 1. Extração
    X_numpy, y_numpy = load_diabetes(return_X_y=True)
    
    # 2. Normalização (Crucial para convergência de gradientes)
    scaler = StandardScaler()
    X_numpy = scaler.fit_transform(X_numpy)
    
    # 3. Conversão para Tensores PyTorch
    X_tensor = torch.tensor(X_numpy, dtype=torch.float32)
    # Redimensiona o target para [N, 1] para parear com a saída da rede
    y_tensor = torch.tensor(y_numpy, dtype=torch.float32).view(-1, 1)
    
    # 4. Particionamento DDP (Data Sharding)
    amostras_totais = len(X_tensor)
    tamanho_lote_local = amostras_totais // world_size
    
    indice_inicio = rank * tamanho_lote_local
    # O último rank absorve qualquer resto de divisão
    indice_fim = indice_inicio + tamanho_lote_local if rank != world_size - 1 else amostras_totais
    
    X_local = X_tensor[indice_inicio:indice_fim]
    y_local = y_tensor[indice_inicio:indice_fim]
    
    return X_local, y_local

def worker_process_lifecycle(rank: int, world_size: int) -> None:
    # Setup de IPC
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '29500'
    dist.init_process_group(backend="gloo", rank=rank, world_size=world_size)

    # Inicialização da topologia
    rede_neural = LinearPredictor(input_dim=10, output_dim=1)
    gerenciador_ddp = MicroDDPOrchestrator(rede_neural)
    
    # Hiperparâmetros
    otimizador = torch.optim.SGD(rede_neural.parameters(), lr=0.1)
    criterio_perda = nn.MSELoss()

    # Carregamento do subconjunto estrito deste processo
    features_locais, labels_locais = preparar_dados_reais(rank, world_size)
    
    print(f"[Rank {rank}] Iniciando com {len(features_locais)} amostras de dados.")

    epocas = 50
    for epoca in range(epocas):
        otimizador.zero_grad()
        
        # Forward Pass
        predicoes = rede_neural(features_locais)
        perda = criterio_perda(predicoes, labels_locais)
        
        # Backward Pass (Cálculo do vetor de gradiente local)
        perda.backward()
        
        # All-Reduce (Média global do gradiente entre todos os Ranks)
        gerenciador_ddp.execute_gradient_reduction()
        
        # Otimização
        otimizador.step()

        # Log a cada 10 épocas para verificação de convergência
        if (epoca + 1) % 10 == 0:
            print(f"[Rank {rank}] Época {epoca+1:02d}/{epocas} | Erro Quadrático Médio (MSE): {perda.item():.2f}")

    dist.destroy_process_group()

if __name__ == "__main__":
    total_workers = 2
    print(f"Inicializando Cluster MicroDDP com {total_workers} processos e dados reais...")
    mp.spawn(
        worker_process_lifecycle,
        args=(total_workers,),
        nprocs=total_workers,
        join=True
    )