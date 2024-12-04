import openai
import os

def retorna_api_key ():
    return os.getenv("OPEN_API_KEY")

# Função para fazer as perguntas e calcular o perfil psicológico
def psychologicalProfile():
  answerUser = []

  #perguntas e opções
  questions = [
      ("Quando te envolves em um novo projeto, qual parte mais te motiva?", 
        ("Desenvolver algo criativo e inovador, transformando ideias em realidade"),
        ("Organizar o projeto e definir metas claras, garantindo que tudo siga um plano"),
        ("Assumir a liderança e tomar decisões rápidas, buscando o sucesso da equipe"),
        ("Trabalhar em colaboração com os outros, criando um ambiente harmônico e produtivo")
      ),
      ("Se precisas resolver um problema complexo, qual é o teu primeiro passo?",
        ("Usar a lógica e uma abordagem prática, resolvendo o problema com soluções técnicas"),
        ("Criar uma abordagem original e fora da caixa, buscando uma solução inovadora"),
        ("Liderar o grupo para encontrar a solução juntos, delegando tarefas e acompanhando o progresso"),
        ("Conversar com outras pessoas para entender diferentes perspectivas, encontrando uma solução colaborativa")
      ),
      ("Em um ambiente de trabalho, como preferes abordar novas tarefas?",
        ("Desenvolvo minhas próprias estratégias e busco inovar, criando algo diferente "),
        ("Prefiro organizar e seguir processos estabelecidos, garantindo que o trabalho seja feito corretamente"),
        ("Tomo a iniciativa e delego responsabilidades, garantindo que todos estejam no caminho certo"),
        ("Gosto de colaborar e ajudar os colegas, promovendo um bom ambiente de trabalho")
      ),
      (" Quando pensas no futuro, qual tipo de carreira te atrai mais?",
        ("Algo onde posso expressar minha criatividade e criar coisas novas, como design ou artes"),
        ("Uma função em que possa liderar e expandir negócios, como gestão ou empreendedorismo"),
        ("Uma carreira onde posso ajudar as pessoas diretamente, como educação ou assistência social"),
        ("Um trabalho técnico e prático que envolva habilidades manuais, como engenharia ou manutenção")
      ),
      ("Ao organizar um evento, o que gostas de fazer?",
        ("Desenvolver o tema e a identidade visual, cuidando da estética e da criatividade do evento"),
        ("Organizar a logística e coordenar os detalhes, garantindo que tudo corra conforme o plano"),
        ("Liderar a equipe e garantir que o evento atinja seu objetivo, motivando os outros a dar o seu melhor"),
        ("Cuidar das pessoas, garantindo que todos se sintam incluídos e confortáveis, promovendo interação e socialização")
      ),
      ("Se fosses convidado a criar um novo produto ou serviço, como abordarias a tarefa?",
        ("Criaria algo inovador e visualmente impactante, com foco na originalidade e no design"),
        ("Lideraria o projeto e buscaria oportunidades de crescimento para o negócio, expandindo o alcance do produto"),
        ("Trabalharia em colaboração com uma equipe diversificada, assegurando que as ideias de todos fossem consideradas"),
        ("Certificaria que o produto fosse funcional e eficiente, com um foco prático e técnico")
      ),
      ("Quando estás a organizar o teu dia, como preferes que ele seja?",
        ("Deixo espaço para a criatividade e a flexibilidade, gostando de variar as tarefas"),
        ("Organizo com horários bem definidos e metas claras, priorizando a eficiência"),
        ("Faço um plano, mas deixo margem para imprevistos, sempre pronto(a) para ajustar conforme necessário"),
        ("Prefiro organizar meu tempo de forma colaborativa, garantindo que posso ajudar e ser ajudado(a)")
      ),
      ("Se fosses trabalhar em um projeto colaborativo, qual seria o teu papel principal?",
        ("Ser a fonte de novas ideias criativas, trazendo inovação ao projeto"),
        ("Liderar a equipe e definir os próximos passos, organizando as atividades"),
        ("Apoiar os outros e garantir que o ambiente de trabalho seja harmonioso, promovendo colaboração"),
        ("Cuidar da parte prática e técnica do projeto, assegurando que tudo funcione corretamente")
      ),
      ("Quando tens uma nova ideia, como costumas colocá-la em prática?",
        ("Exploro formas criativas e inovadoras para desenvolvê-la, buscando originalidade"),
        ("Faço um plano detalhado e sigo uma metodologia organizada, garantindo que a ideia seja implementada corretamente"),
        (" Tomo a iniciativa e coordeno os outros para ajudar a desenvolver a ideia, focando em sua expansão e crescimento"),
        ("Discuto com outras pessoas para obter feedback e aperfeiçoar a ideia, buscando diferentes perspectivas")
      ),
      ("Como preferes abordar situações de risco ou desafios?",
        ("Tomo a iniciativa e aceito o risco, enxergando-o como uma oportunidade de crescimento"),
        ("Analiso cuidadosamente as possíveis consequências, preferindo seguir um plano estruturado"),
        ("Busco uma solução criativa para superar o desafio, inovando nas minhas abordagens"),
        ("Converso com os outros e trabalho em conjunto para encontrar a melhor solução, compartilhando responsabilidades")
        ),
      ("Como preferes lidar com tarefas que exigem atenção aos detalhes?",
        ("Gosto de seguir um plano ou um processo estruturado, garantindo que tudo esteja dentro dos padrões"),
        ("Verifico a eficiência prática da tarefa, assegurando que tudo esteja a funcionar corretamente"),
        ("Analiso os detalhes para entender o porquê das coisas, questionando e explorando os dados com profundidade"),
        ("Concluo a tarefa rapidamente, sem me preocupar tanto com os detalhes.")
        ),
        ("Como te sentes ao trabalhar com números, dados ou códigos?",
        ("Sinto-me confortável e organizado(a), gosto de sistemas que seguem uma lógica clara"),
        ("Vejo números e códigos como uma ferramenta prática para resolver problemas, usando-os para alcançar resultados concretos"),
        ("Adoro analisar e interpretar dados profundamente, buscando padrões e novas descobertas"),
        ("Prefiro não lidar com números ou dados, é algo que evito.")
        ),
        ("Ao resolver problemas técnicos, qual é o teu método preferido?",
        ("Sigo um manual ou um procedimento já estabelecido, gosto de ter instruções claras"),
        ("Testo diferentes abordagens práticas até encontrar a solução, focando no funcionamento eficaz"),
        ("Investigo a fundo para entender o problema antes de tentar qualquer solução, analisando todas as variáveis"),
        ("Prefiro deixar que outra pessoa resolva, pois não me sinto à vontade com problemas técnicos.")
        ),
        ("Se precisas organizar uma grande quantidade de informações, como procedes?",
        ("Classifico as informações de forma estruturada e organizada, criando listas ou tabelas para facilitar o acesso"),
        ("Seleciono as informações mais relevantes e foco no que é prático e funcional, eliminando o que é desnecessário"),
        ("Analiso cuidadosamente as informações para encontrar padrões e gerar novas conclusões, fazendo conexões entre os dados"),
        ("Prefiro não lidar com tantas informações de uma vez, delego para outra pessoa.")
        ),
        ("Quando enfrentas uma nova tecnologia ou ferramenta, como reages?",
        ("Leio o manual ou instruções antes de usar, prefiro seguir um guia estruturado"),
        ("Começo a usar a tecnologia imediatamente para ver como funciona na prática"),
        ("Investigo como a tecnologia foi desenvolvida e tento entender sua lógica de funcionamento, buscando compreender profundamente"),
        ("Só uso a nova tecnologia se for absolutamente necessário, caso contrário, evito.")
        )
  ]

  for i, question in enumerate(questions, start=1):
    print(f"\nPergunta {i}: {question[0]}")
    for j, option in enumerate(question[1:], start=1):
        print(f"{j}. {option}")
    
    # Obter a escolha do utilizador
    while True:
        try:
          choice = int(input("Escolha uma opção (1-4): "))
          if 1 <= choice <= len(question[1:]):
              answerUser.append(question[choice])   # Adicionar a resposta escolhida
              break
          else:
              print("Por favor, escolha um número válido.")
        except ValueError:
          print("Entrada inválida. Digite apenas o número da opção.")

  return answerUser


# Analisa as respostas do utilizador e define o perfil correspondente
def analisar_respostas(respostas):
    openai.api_key = retorna_api_key()
    if not openai.api_key:
        raise ValueError("Erro de validação de key")
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{
        "role": "system", "content": f"Com base nas seguintes respostas: {', '.join(respostas)}, classifique o perfil do usuário no modelo RIASEC."
        }],
        max_tokens=150
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    respostas = psychologicalProfile()
    perfil = analisar_respostas(respostas)
    print(f"Perfil identificado: {perfil}")
