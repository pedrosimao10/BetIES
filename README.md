# ProjetoIES
Projeto Final de IES

## Roles:

- Team Manager: Afonso Rodrigues (NMEC: 93124)
- Architect: Gonçalo Pereira (NMEC: 93310)
- DevOps Master: Alexandre Pinto (NMEC: 98401)
- Product Owner: Pedro Jorge (NMEC: 98418)


## Backlog

Foi utilizado o Jira para fazer o backlog: https://afonso1666.atlassian.net/jira/software/projects/IES/boards/1


## How to Run the WebSite

1. cd betIES -> mvn clean package -DskipTests -> cd ..
2. sudo docker-compose build
3. sudo docker-compose down -v
4. sudo docker-compose up
5. Access:
  - http://localhost:2020/user/user
  or
  - http://localhost:2020/admin/admin
  or
  - http://localhost:2020/employee/employee
