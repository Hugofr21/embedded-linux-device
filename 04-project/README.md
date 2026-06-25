# 12. Problemas mais importantes para Embedded Linux

<pre class="overflow-visible! px-0!" data-start="3838" data-end="4011"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>1. Buffer Overflow</span><br/><span>2. Use After Free</span><br/><span>3. Race Condition</span><br/><span>4. Deadlock</span><br/><span>5. Memory Leak</span><br/><span>6. Integer Overflow</span><br/><span>7. Heap Corruption</span><br/><span>8. Rootkits</span><br/><span>9. MMU e proteção de memória</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></div></pre>

Ferramentas normalmente usadas para detetar estes problemas:

* **clang-tidy**
* **Valgrind**
* **AddressSanitizer**
* **ThreadSanitizer**
* **GDB**
* **cppcheck**
