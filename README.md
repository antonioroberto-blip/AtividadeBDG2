Projeto desenvolvido para a disciplina Banco de Dados Avançados.

Tecnologias Usadas:
- Python
- MongoDB Atlas
- PyMongo
- Faker

O projeto utiliza três coleções:
- cursos
- alunos
- matriculas

Cada matrícula possui:
- aluno_id
- curso_id
- data_matricula
- progresso
- concluida
- nota, quando o curso é concluído

As matrículas usam referências para alunos e cursos.
Essa abordagem evita aumentar excessivamente o documento de curso e
facilita consultar e alterar as matrículas.

O MongoDB possui limite de 16 MB por documento.
Por isso, não é adequado colocar uma quantidade potencialmente muito
grande de matrículas dentro de um único documento de curso.

A coleção cursos possui validação para:
- título obrigatório
- categoria obrigatória
- preço maior ou igual a zero
- vagas maior ou igual a zero
- módulos como array

Um curso com preço negativo é rejeitado.

Como executar:

Instale as dependências:
pip install -r requirements.txt

Configure o arquivo .env:
MONGO_URI=sua_uri
MONGO_DB=aprenda_mais

Execute a validação:
python validacao.py

Execute a carga inicial:
python seed.py

Execute o programa:
python main.py

O seed remove os dados existentes antes de criar uma nova carga.
Assim, executar o script novamente não gera duplicação dos dados.

Pergunta do Professor no README:
"Em que situação embutir as matrículas dentro do documento do curso seria um erro de modelagem?"

Seria um erro quando um curso pudesse possuir muitas matrículas ou
quando as matrículas precisassem ser consultadas e atualizadas
individualmente com frequência.
Nesse caso, colocar todas as matrículas dentro do documento do curso
poderia fazer o documento crescer demais e dificultar as operações.
Por isso, neste projeto as matrículas ficam em uma coleção própria e
referenciam o aluno e o curso.
