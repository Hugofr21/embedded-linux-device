import torch
import torch.distributed as dist

class MicroDDPOrchestrator:
    """
    Encapsula as primitivas de rede (All-Reduce) necessárias para sincronização.
    """
    def __init__(self, model: torch.nn.Module):
        self.model = model
        self._enforce_deterministic_weights()

    def _enforce_deterministic_weights(self) -> None:
        """Sincroniza os pesos iniciais a partir do Rank 0 via broadcast."""
        if dist.is_initialized():
            for parameter in self.model.parameters():
                if parameter.requires_grad:
                    dist.broadcast(parameter.data, src=0)

    def execute_gradient_reduction(self) -> None:
        """Aplica a média global de gradientes através de barreira síncrona."""
        if not dist.is_initialized():
            return
            
        cluster_size = dist.get_world_size()
        for parameter in self.model.parameters():
            if parameter.requires_grad and parameter.grad is not None:
                # Operação de comunicação coletiva síncrona
                dist.all_reduce(parameter.grad.data, op=dist.ReduceOp.SUM)
                parameter.grad.data /= cluster_size