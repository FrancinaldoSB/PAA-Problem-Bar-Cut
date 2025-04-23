import time as t
import matplotlib.pyplot as plt
import numpy as np
import gc
from functools import lru_cache
import seaborn as sns
import tracemalloc
import os

precos = [0, 1, 5, 8, 9, 10, 17, 17, 20]
comp1 = 45

def corte_recursivo(precos, n):
    @lru_cache(maxsize=None)
    def helper(n):
        if n == 0:
            return 0, []
        max_lucro = float('-inf')
        melhor_corte = []
        for i in range(1, n + 1):
            if i < len(precos):
                lucro, cortes = helper(n - i)
                lucro_atual = precos[i] + lucro
                if lucro_atual > max_lucro:
                    max_lucro = lucro_atual
                    melhor_corte = [i] + cortes
        return max_lucro, melhor_corte
    resultado = helper(n)
    helper.cache_clear()
    gc.collect()
    return resultado

def corte_dinamico(precos, n):
    dp = [0] * (n + 1)
    cortes = [-1] * (n + 1)

    for j in range(1, n + 1):
        max_lucro = float('-inf')
        for i in range(1, min(j + 1, len(precos))):
            if precos[i] + dp[j - i] > max_lucro:
                max_lucro = precos[i] + dp[j - i]
                cortes[j] = i
        dp[j] = max_lucro if max_lucro != float('-inf') else 0

    resultado_cortes = []
    comprimento_atual = n
    while comprimento_atual > 0 and cortes[comprimento_atual] != -1:
        resultado_cortes.append(cortes[comprimento_atual])
        comprimento_atual -= cortes[comprimento_atual]

    return dp[n], resultado_cortes

def coletar_tempos(algoritmo, precos, comp, repeticoes=100):
    tempos = []
    for _ in range(repeticoes):
        inicio = t.time()
        algoritmo(precos, comp)
        fim = t.time()
        duracao = fim - inicio
        if duracao > 0:
            tempos.append(duracao)
        gc.collect()
    return tempos

def coletar_memoria(algoritmo, precos, comp):
    tracemalloc.start()
    algoritmo(precos, comp)
    mem_atual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return mem_atual, mem_pico
    
def remover_outliers(valores):
    q1 = np.percentile(valores, 25)
    q3 = np.percentile(valores, 75)
    iqr = q3 - q1
    lim_inferior = q1 - 1.5 * iqr
    lim_superior = q3 + 1.5 * iqr
    return [v for v in valores if lim_inferior <= v <= lim_superior]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    lucro_recursivo, cortes_recursivo = corte_recursivo(precos, comp1)
    
    lucro_dinamico, cortes_dinamico = corte_dinamico(precos, comp1)

    print("RESULTADOS")
    print(f"Comprimento da barra: {comp1}")
    print(f"Tabela de precos: {precos[1:]}")
    print("\nRecursivo:")
    print(f"Valor maximo obtido: {lucro_recursivo}")
    print(f"Quantidade de cortes: {len(cortes_recursivo)}")
    print(f"Cortes otimos: {cortes_recursivo}")
    
    print("\nDinâmico:")
    print(f"Valor maximo obtido: {lucro_dinamico}")
    print(f"Quantidade de cortes: {len(cortes_dinamico)}")
    print(f"Cortes otimos: {cortes_dinamico}")
    
    input("Pressione qualquer tecla para continuar...")
    clear()
    
    print("MEMÓRIA")
    mem_atual, mem_pico = coletar_memoria(corte_dinamico, precos, comp1)
    print("Dinamico:")
    print(f"Memória atual: {mem_atual / 1024:.2f} KB")
    print(f"Pico de memória: {mem_pico / 1024:.2f} KB")
    mem_atual, mem_pico = coletar_memoria(corte_recursivo, precos, comp1)
    print("\nRecursivo:")
    print(f"Memória atual: {mem_atual / 1024:.2f} KB")
    print(f"Pico de memória: {mem_pico / 1024:.2f} KB")
    
    input("Coletando tempos e plotando o gráfico...")
    clear()
    
    print("\nGRÁFICOS")
    print("Plotando os gráficos...")
    
    tempos_dinamico = coletar_tempos(corte_dinamico, precos, comp1, repeticoes=100)
    tempos_recursivo = coletar_tempos(corte_recursivo, precos, comp1, repeticoes=100)

    tempos_recursivo_filtrados = remover_outliers(tempos_recursivo)
    tempos_dinamico_filtrados = remover_outliers(tempos_dinamico)

    palette = sns.color_palette("pastel", n_colors=2)

    # Paleta pastel do Seaborn
    palette = sns.color_palette("pastel", n_colors=2)

    # Gerar o gráfico
    plt.figure(figsize=(10, 6))

    box = plt.boxplot(
        [tempos_recursivo_filtrados, tempos_dinamico_filtrados],
        tick_labels=["Recursivo", "Dinâmico"],  # Corrigido de 'labels' para 'tick_labels'
        patch_artist=True,
        showfliers=False
    )

    # Pintar os boxes com cores pastéis
    for patch, color in zip(box['boxes'], palette):
        patch.set_facecolor(color)

    # Pintar a linha da mediana de preto
    for median in box['medians']:
        median.set_color('black')
        median.set_linewidth(1)

    # Estética
    plt.title(f"Boxplot dos tempos de execução (Comprimento {comp1})")
    plt.ylabel("Tempo (s)")
    plt.grid(True)
    plt.show()
    
    print("Gráficos plotados com sucesso...")