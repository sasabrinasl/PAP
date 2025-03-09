import openai
import os
import mysql.connector                                                   
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.secret_key = "chave_secreta"

def retorna_api_key():
  api_key = os.getenv("OPEN_API_KEY")

#perguntas e opções
questionsAndOptions = [
  { "question": "Quando te envolves em um novo projeto, qual parte mais te motiva?", 
    "options": [
    "Desenvolver algo criativo e inovador, transformando ideias em realidade",
    "Organizar o projeto e definir metas claras, garantindo que tudo siga um plano",
    "Assumir a liderança e tomar decisões rápidas, buscando o sucesso da equipe",
    "Trabalhar em colaboração com os outros, criando um ambiente harmônico e produtivo"]
  },
  { "question": "Se precisas resolver um problema complexo, qual é o teu primeiro passo?",
    "options": [
    "Usar a lógica e uma abordagem prática, resolvendo o problema com soluções técnicas",
    "Criar uma abordagem original e fora da caixa, buscando uma solução inovadora",
    "Liderar o grupo para encontrar a solução juntos, delegando tarefas e acompanhando o progresso",
    "Conversar com outras pessoas para entender diferentes perspectivas, encontrando uma solução colaborativa"]
  },
  { "question": "Em um ambiente de trabalho, como preferes abordar novas tarefas?",
    "options": [
    "Desenvolvo minhas próprias estratégias e busco inovar, criando algo diferente",
    "Prefiro organizar e seguir processos estabelecidos, garantindo que o trabalho seja feito corretamente",
    "Tomo a iniciativa e delego responsabilidades, garantindo que todos estejam no caminho certo",
    "Gosto de colaborar e ajudar os colegas, promovendo um bom ambiente de trabalho"]
  },
  { "question": "Quando pensas no futuro, qual tipo de carreira te atrai mais?",
    "options": [
    "Algo onde posso expressar minha criatividade e criar coisas novas, como design ou artes",
    "Uma função em que possa liderar e expandir negócios, como gestão ou empreendedorismo",
    "Uma carreira onde posso ajudar as pessoas diretamente, como educação ou assistência social",
    "Um trabalho técnico e prático que envolva habilidades manuais, como engenharia ou manutenção"]
  },
  { "question": "Ao organizar um evento, o que gostas de fazer?",
    "options": [
    "Desenvolver o tema e a identidade visual, cuidando da estética e da criatividade do evento",
    "Organizar a logística e coordenar os detalhes, garantindo que tudo corra conforme o plano",
    "Liderar a equipe e garantir que o evento atinja seu objetivo, motivando os outros a dar o seu melhor",
    "Cuidar das pessoas, garantindo que todos se sintam incluídos e confortáveis, promovendo interação e socialização"]
  },
  { "question": "Se fosses convidado a criar um novo produto ou serviço, como abordarias a tarefa?",
    "options": [
    "Criaria algo inovador e visualmente impactante, com foco na originalidade e no design",
    "Lideraria o projeto e buscaria oportunidades de crescimento para o negócio, expandindo o alcance do produto",
    "Trabalharia em colaboração com uma equipe diversificada, assegurando que as ideias de todos fossem consideradas",
    "Certificaria que o produto fosse funcional e eficiente, com um foco prático e técnico"]
  },
  { "question": "Quando estás a organizar o teu dia, como preferes que ele seja?",
    "options": [
    "Deixo espaço para a criatividade e a flexibilidade, gostando de variar as tarefas",
    "Organizo com horários bem definidos e metas claras, priorizando a eficiência",
    "Faço um plano, mas deixo margem para imprevistos, sempre pronto(a) para ajustar conforme necessário",
    "Prefiro organizar meu tempo de forma colaborativa, garantindo que posso ajudar e ser ajudado(a)"]
  },
  { "question": "Se fosses trabalhar em um projeto colaborativo, qual seria o teu papel principal?",
    "options": [
    "Ser a fonte de novas ideias criativas, trazendo inovação ao projeto",
    "Liderar a equipe e definir os próximos passos, organizando as atividades",
    "Apoiar os outros e garantir que o ambiente de trabalho seja harmonioso, promovendo colaboração",
    "Cuidar da parte prática e técnica do projeto, assegurando que tudo funcione corretamente"]
  },
  { "question": "Quando tens uma nova ideia, como costumas colocá-la em prática?",
    "options": [
    "Exploro formas criativas e inovadoras para desenvolvê-la, buscando originalidade",
    "Faço um plano detalhado e sigo uma metodologia organizada, garantindo que a ideia seja implementada corretamente",
    "Tomo a iniciativa e coordeno os outros para ajudar a desenvolver a ideia, focando em sua expansão e crescimento",
    "Discuto com outras pessoas para obter feedback e aperfeiçoar a ideia, buscando diferentes perspectivas"]
  },
  { "question": "Como preferes abordar situações de risco ou desafios?",
    "options": [
    "Tomo a iniciativa e aceito o risco, enxergando-o como uma oportunidade de crescimento",
    "Analiso cuidadosamente as possíveis consequências, preferindo seguir um plano estruturado",
    "Busco uma solução criativa para superar o desafio, inovando nas minhas abordagens",
    "Converso com os outros e trabalho em conjunto para encontrar a melhor solução, compartilhando responsabilidades"]
  },
  { "question": "Como preferes lidar com tarefas que exigem atenção aos detalhes?",
    "options": [
    "Gosto de seguir um plano ou um processo estruturado, garantindo que tudo esteja dentro dos padrões",
    "Verifico a eficiência prática da tarefa, assegurando que tudo esteja a funcionar corretamente",
    "Analiso os detalhes para entender o porquê das coisas, questionando e explorando os dados com profundidade",
    "Concluo a tarefa rapidamente, sem me preocupar tanto com os detalhes."]
  },
  { "question": "Como te sentes ao trabalhar com números, dados ou códigos?",
    "options": [
    "Sinto-me confortável e organizado(a), gosto de sistemas que seguem uma lógica clara",
    "Vejo números e códigos como uma ferramenta prática para resolver problemas, usando-os para alcançar resultados concretos",
    "Adoro analisar e interpretar dados profundamente, buscando padrões e novas descobertas",
    "Prefiro não lidar com números ou dados, é algo que evito."]
  },
  { "question": "Ao resolver problemas técnicos, qual é o teu método preferido?",
    "options": [
    "Sigo um manual ou um procedimento já estabelecido, gosto de ter instruções claras",
    "Testo diferentes abordagens práticas até encontrar a solução, focando no funcionamento eficaz",
    "Investigo a fundo para entender o problema antes de tentar qualquer solução, analisando todas as variáveis",
    "Prefiro deixar que outra pessoa resolva, pois não me sinto à vontade com problemas técnicos."]
  },
  { "question": "Se precisas organizar uma grande quantidade de informações, como procedes?",
    "options": [
    "Classifico as informações de forma estruturada e organizada, criando listas ou tabelas para facilitar o acesso",
    "Seleciono as informações mais relevantes e foco no que é prático e funcional, eliminando o que é desnecessário",
    "Analiso cuidadosamente as informações para encontrar padrões e gerar novas conclusões, fazendo conexões entre os dados",
    "Prefiro não lidar com tantas informações de uma vez, delego para outra pessoa."]
  },
  { "question": "Quando enfrentas uma nova tecnologia ou ferramenta, como reages?",
    "options": [
    "Leio o manual ou instruções antes de usar, prefiro seguir um guia estruturado",
    "Começo a usar a tecnologia imediatamente para ver como funciona na prática",
    "Investigo como a tecnologia foi desenvolvida e tento entender sua lógica de funcionamento, buscando compreender profundamente",
    "Só uso a nova tecnologia se for absolutamente necessário, caso contrário, evito."]
  }
]

user_responses = []
current_question_index = 0

# Configurar banco de dados 
db_config = {
  'host': 'localhost',
  'user': 'root',
  'password': 'rootsabrina',
  'database': 'login'
}

# Conectar ao banco de dados
def connect_db():
  return mysql.connector.connect(**db_config)

# Criar banco de dados e tabela 
def start_db():
    conn = mysql.connector.connect(host=db_config['host'], user=db_config['user'], password=db_config['password'])
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS login")
    conn.database = 'login'

    cursor.execute("""
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE)
    """)

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    session["current_question"] = 0  # Inicia o índice das perguntas
    session["user_responses"] = []  # Lista para armazenar respostas
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def save_data():
    nome = request.form['nome']
    email = request.form['email']

    try:
      conn = connect_db()
      cursor = conn.cursor()

      sql = 'INSERT INTO users (name, email) VALUES (%s, %s)'
      valores = (nome, email)

      cursor.execute(sql, valores)
      conn.commit()

      # Exibir os dados no terminal
      cursor.execute("SELECT * FROM users")
      resultados = cursor.fetchall()  # Obtém todos os registros
      print("\nDados cadastrados na tabela 'users':")
      for row in resultados:
          print(f"ID: {row[0]} | Nome: {row[1]} | E-mail: {row[2]}")
      
      cursor.close()
      conn.close()
      
      return redirect(url_for('test'))

    except mysql.connector.Error as err:
        return f"Erro ao inserir dados: {err}"

@app.route("/test", methods=["GET", "POST"])
def test():
    if "current_question" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        answer = request.form.get("answer")
        session["user_responses"].append({
            "pergunta": questionsAndOptions[session["current_question"]]["question"],
            "resposta": answer
        })
        session["current_question"] += 1

        # Se todas as perguntas foram respondidas, redireciona para a análise
        if session["current_question"] >= len(questionsAndOptions):
            return redirect(url_for("analyze"))

    question_index = session["current_question"]
    question_data = questionsAndOptions[question_index]

    return render_template("test.html", question=question_data["question"], options=question_data["options"])

@app.route('/analyze', methods=['GET'])
def analyze():
    perfil_percentagens = analisar_respostas(session["user_responses"])
    session["perfil_percentagens"] = perfil_percentagens  # Salva os resultados
    return redirect(url_for("result_page"))  # Redireciona para a página de resultados

@app.route('/resultPage', methods=['POST'])
def result_page():
    perfil = request.args.get('perfil', 'Indefinido')  # Obtém o perfil da URL
    return render_template('result.html', perfil=perfil)  # Envia para o HTML

# Analisa as respostas do utilizador e define o perfil correspondente
def analisar_respostas(finalAnswers):
    openai.api_key = retorna_api_key()
    if not openai.api_key:
        raise ValueError("Erro de validação de key")
    
    answerText = '\n'.join([f"Pergunta: {ans['pergunta']}\nResposta:{ans['resposta']}" for ans in finalAnswers])
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
          {
            "role": "system",
            "content": "És um especialista na aplicação da teoria RIASEC de John Holland, que avalia perfis psicológicos com base em respostas e perguntas. Analise o seguinte:"
          },
          {
            "role": "user",
            "content": f"As respostas do utilizador são:\n\n{answerText}\n\nClassifique o perfil o perfil no modelo RIASEC com base nestas informações, entregando apenas o perfil prevalecente escrito por extenso, sem dar uma descrição ou explicação."
          }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    start_db()
    app.run(debug=True)
