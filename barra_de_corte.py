def corte_de_barra_dinamico(precos, n):
    """
    Resolve o problema do corte de barra usando programação dinâmica.
    
    Args:
        precos: Lista de preços onde precos[i] é o preço para um pedaço de tamanho i+1
        n: Comprimento total da barra
        
    Returns:
        O valor máximo obtido e a lista de cortes ótimos
    """
    
    dp = [0] * (n + 1)
    
    cortes = [0] * (n + 1)
    
    for i in range(1, n + 1):
        max_valor = -float('inf')
        for j in range(1, i + 1):
            if j <= len(precos):
                if precos[j-1] + dp[i-j] > max_valor:
                    max_valor = precos[j-1] + dp[i-j]
                    cortes[i] = j 
        dp[i] = max_valor

    solucao = []
    tamanho_restante = n
    while tamanho_restante > 0:
        corte = cortes[tamanho_restante]
        solucao.append(corte)
        tamanho_restante -= corte
    
    return dp[n], solucao

def corte_de_barra_recursivo(precos, n):
    """
    Resolve o problema do corte de barra usando recursão.
    
    Args:
        precos: Lista de preços onde precos[i] é o preço para um pedaço de tamanho i+1
        n: Comprimento total da barra
        
    Returns:
        O valor máximo obtido e a lista de cortes ótimos
    """

    if n == 0:
        return 0, []
    
    max_valor = -float('inf')
    melhor_corte = []
    
    for j in range(1, min(n, len(precos)) + 1):
        valor_atual, cortes_atual = corte_de_barra_recursivo(precos, n - j)
        valor_total = precos[j-1] + valor_atual
        
        if valor_total > max_valor:
            max_valor = valor_total
            melhor_corte = [j] + cortes_atual
    
    return max_valor, melhor_corte

if __name__ == "__main__":
    precos = [3, 5, 8, 5, 10]
    comprimento = 4
    
    valor_maximo_din, cortes_otimos_din = corte_de_barra_dinamico(precos, comprimento)
    
    print("Dinamico:")
    print(f"Comprimento da barra: {comprimento}")
    print(f"Tabela de preços: {precos}")
    print(f"Valor máximo obtido: {valor_maximo_din}")
    print(f"Cortes ótimos: {cortes_otimos_din}")

    valor_maximo_rec, cortes_otimos_rec = corte_de_barra_recursivo(precos, comprimento)

    print("Recursivo:")
    print(f"Comprimento da barra: {comprimento}")
    print(f"Tabela de preços: {precos}")
    print(f"Valor máximo obtido: {valor_maximo_rec}")
    print(f"Cortes ótimos: {cortes_otimos_rec}")