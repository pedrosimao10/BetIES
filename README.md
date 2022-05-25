# ProjetoIES
Projeto Final de IES

## Concept:
Each group is expected to propose, conceptualize, and implement a multi-layer, enterprise-class application. 
We decided to do a Betting Web Application where the user can place bets and each odd is constantly being updated. To do this we developed a Data Genarator.

## Technologies Used:
- HTML;
- CSS;
- JavaScript;
- Python;
- Java;
- Thymeleaf.

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
