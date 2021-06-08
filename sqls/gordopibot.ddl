drop table IF EXISTS usuarios_aperturas;
drop table IF EXISTS usuarios_partidas;
drop table IF EXISTS partidas;
drop table IF EXISTS  usuarios;
drop table IF EXISTS categorias_usuario;
drop table IF EXISTS aperturas_local;
drop table IF EXISTS categorias_usuario;




CREATE TABLE categorias_usuario(
	codigo char(2),
	descripcion varchar(20),
	constraint cateria_usuarios_pk PRIMARY KEY (codigo)
);


CREATE TABLE usuarios(
       id INTEGER UNSIGNED,
       nombre varchar(50),
       categoria char(2),
       constraint usuarios_pk PRIMARY KEY (id),
       constraint usuarios_categoria_fk FOREIGN KEY (categoria) REFERENCES categorias_usuario(codigo)     
);


CREATE TABLE aperturas_local(
       id SERIAL,
       fechaApertura DATETIME,
       fechaCierre DATETIME,
       constraint aperturas_local_pk PRIMARY KEY (id)
       
);


CREATE TABLE usuarios_aperturas(
       idUsuario INTEGER UNSIGNED,
       idApertura BIGINT UNSIGNED,
       constraint usuario_apertura_usuario_fk FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
       constraint usuario_apertura_apertura_fk FOREIGN KEY (idApertura) REFERENCES aperturas_local(id)
);


CREATE TABLE partidas (
	id SERIAL,
	nombre varchar(100),
	idJuego INTEGER UNSIGNED,
	idApertura BIGINT UNSIGNED,
	idCreador INTEGER UNSIGNED,
	plazas INTEGER UNSIGNED,
	constraint partidas_pk PRIMARY KEY (id),
	constraint partidas_usuario_fk  FOREIGN KEY (idCreador) REFERENCES usuarios(id),
     constraint partidas_apertura_fk FOREIGN KEY (idApertura) REFERENCES aperturas_local(id)
	
);

CREATE TABLE usuarios_partidas(
       idUsuario INTEGER UNSIGNED,
       idPartida BIGINT UNSIGNED,
       constraint usuario_partidas_usuario_fk FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
       constraint usuario_partidas_partidas_fk FOREIGN KEY (idPartida) REFERENCES partidas(id)
);


INSERT INTO categorias_usuario values ('AD','Administrador');
INSERT INTO categorias_usuario values ('SP','Socio de Pago');
INSERT INTO categorias_usuario values ('SJ','Socio junior');
INSERT INTO categorias_usuario values ('JU','Jugón');

--INSERT INTO usuarios values (709463079,'Alfredo','AD');



