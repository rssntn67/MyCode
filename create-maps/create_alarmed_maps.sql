create table alarmed_map (
    mapId                        integer not null,
    mapName                      varchar(40) not null,
    mapBackGround        varchar(256),
    mapOwner             varchar(64) not null,
    mapCreateTime        timestamp not null,
    mapAccess            char(6) not null,
    userLastModifies varchar(64) not null,
    lastModifiedTime timestamp not null,
    mapScale         float8,
    mapXOffset      integer,
        mapYOffset       integer,
        mapType          char(1),
        mapWidth                integer not null,
        mapHeight               integer not null,

        constraint pk_alarmed_mapID primary key (mapId)
);

create table alarmed_element (
    mapId                        integer not null,
    elementId            integer not null,
        elementType      char(1) not null,
    elementLabel         varchar(256) not null,
    elementIcon          varchar(256),
    elementX         integer,
        elementY         integer,

        constraint fk_alarmed_mapID foreign key (mapId) references alarmed_map on delete cascade
);

alter table alarmed_element add constraint pk_element primary key (mapId,elementId,elementType);
alter table alarmed_element add constraint elementid check (elementid <> 0);
