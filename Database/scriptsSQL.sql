use betIES;

drop table historico_bet;
drop table historico;
drop table bet;
drop table jogos;
drop table equipas;
drop table ligas;
drop table desportos;
drop table admins;
drop table func;
drop table users;


if OBJECT_ID(N'users', N'U') IS NULL begin
create table users(
    Username varchar(255)		unique,
    FirstName varchar(255),
    LastName varchar(255),
    [Password] varchar(255),
    Email varchar(255)			unique,
    Primary KEY (Email)

);

INSERT into users
values('Afonso166', 'Afonso', 'Rodrigues', 'pass12345', 'afonsor@ua.pt');
end

if OBJECT_ID(N'func', N'U') IS NULL begin
create table func(
    FuncID varchar(255),
    FirstName varchar(255),
    LastName varchar(255),
    [Password] varchar(255),
    Email varchar(255)			unique,
    Primary KEY (FuncID)
);

INSERT into func
values('111', 'Gonçalo', 'Pereira', 'pass67890', 'goncalop@ua.pt');
end

if OBJECT_ID(N'admins', N'U') IS NULL begin
create table admins(
    AdminID varchar(255),
    FirstName varchar(255),
    LastName varchar(255),
    [Password] varchar(255),
    Email varchar(255)			unique,
    Primary KEY (AdminID)
);

INSERT into admins
values('222', 'Gonçalo', 'Pereira', 'pass13579', 'goncalop2@ua.pt');
end

if OBJECT_ID(N'desportos', N'U') IS NULL begin
create table desportos (
	id int NOT NULL	IDENTITY,
	nome varchar(255)		unique,
	primary key (id)
);
end

if OBJECT_ID(N'ligas', N'U') IS NULL begin
create table ligas (
	id int NOT NULL	IDENTITY,
	nome varchar(255),
	desporto int,
	foreign key (desporto) references desportos(id),
	primary key (id)
);
end

if OBJECT_ID(N'equipas', N'U') IS NULL begin
create table equipas (
	id int NOT NULL	IDENTITY,
	nome varchar(255),
	desporto int,
	liga int,
	foreign key (desporto) references desportos(id),
	foreign key (liga) references ligas(id),
	primary key (id)
);
end

if OBJECT_ID(N'jogos', N'U') IS NULL begin
create table jogos (
	id int NOT NULL	IDENTITY,
	equipa1 int,
	equipa2 int,
	odd1 decimal(5,2),
	odd2 decimal(5,2),
	odd3 decimal(5,2),
	hora datetime,
	final bit,
	foreign key (equipa1) references equipas(id),
	foreign key (equipa2) references equipas(id),
	primary key (id)
);
end

if OBJECT_ID(N'bet', N'U') IS NULL begin
create table bet (
	id int NOT NULL	IDENTITY,
	[user] varchar (255),
	jogo int,
	resultado int,
	foreign key ([user]) references users(Email),
	foreign key (jogo) references jogos(id),
	primary key(id)
);
end

if OBJECT_ID(N'historico', N'U') IS NULL begin
create table historico(
	id int NOT NULL	IDENTITY,
	[user] varchar (255),
	foreign key ([user]) references users(Email),
	primary key (id)
);
end

if OBJECT_ID(N'historico_bet', N'U') IS NULL begin
create table historico_bet (
	historico int,
	bet int,
	foreign key (historico) references historico(id),
	foreign key (bet) references bet(id),
	primary key (historico, bet)
);
end