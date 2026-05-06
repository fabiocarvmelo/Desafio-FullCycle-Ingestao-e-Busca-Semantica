from search import search_prompt

def main():
    # inicia a chain de busca
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("--- Chat IA iniciado (digite 'sair' para encerrar) ---")

    pergunta = input("\n>>> Faça sua pergunta: \n")
    
    while True:

        if pergunta.lower() == "sair":
            print("Encerrando o chat. Até mais!")
            break
        
        try:
            # executa a consulta
            print("\nProcessando sua pergunta...")
            resposta = chain.invoke(pergunta)
            print(f"\n>>> Resposta: \n{resposta}")
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")

        pergunta = input("\n>>> Faça uma nova pergunta: \n")

if __name__ == "__main__":
    main()