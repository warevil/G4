entity "Usuario" as U {
  * usuario_id: int <<PK>>
  --
  * nombre_completo: string
  * email: string
  * foto: string
}

entity "Usuario-Curso" as UC {
  * usuario_id: int <<PK>> <<FK>>
  * curso_id: int <<PK>> <<FK>>
  --
  * rol: string
  * estado: string
}

entity "Curso" as C {
  * curso_id: int <<PK>>
  --
  * creador_id: int <<FK>>
  * titulo: string
  * descripcion: string
}

entity "Grupo-Alumno" as GA{
  * grupo_id: int <<PK>> <<FK>>
  * alumno_id: int <<PK>> <<FK>>
  --
  * coordinador: bool
}

entity "Grupo" as G {
  * grupo_id: int <<PK>>
  --
  * curso_id: int <<FK>>
  * public_id: int
}

entity "Tarea-Grupo" as TG {
  * evaluacion_id: int <<PK>>
  --
  * tarea_id: int <<FK>>
  * grupo_id: int <<FK>>
  * archivos_solucion: strings[]
  * nota: int
}

entity "Tarea-Alumno" as TA{
  * evaluacion_id: int <<PK>>
  --
  * alumno_id: int <<FK>>
  * tarea_id: int <<FK>>
  * nota: int
  * archivos_solucion: strings[]
}

entity "Examen-Alumno" as EA {
  * evaluacion_id: int <<PK>>
  --
  * alumno_id: int <<FK>>
  * examen_id: int <<FK>>
  * archivos_solucion: strings[]
  * nota: int
}

entity "Comentario" as Co {
  * comentario_id: int <<PK>>
  --
  * publicacion_id: int <<FK>>
  * autor_id: int <<FK>>
  * contenido: string
  * likes_num: int
  * dislikes_num: int
  * esRespuesta: bool
}

entity "Respuestas" as Re {
  * comentario_id: int <<PK>> <<FK>>
  * respuesta_id: int <<PK>> <<FK>>
  --
}

entity "Publicacion" as Pub {
  * publicacion_id: int <<PK>>
  --
  * autor_id: int <<FK>>
  * curso_id: int <<FK>>
  * titulo: string
  * descripcion: string
}

entity "Evaluacion" as T {
  --
  * tipo: string
  * max_puntos:int
  * fecha_max: date
  * archivos_publicados: strings[]
}

entity "Material" as M {
  --
  * archivos_publicados: strings[]
}

' Relations


Pub <|-- M
Pub <|-- T


U ||..o{ UC
UC }o..|| C
TG }o..|| G
T  ||..o{ TG
TA }o..|| U
T  ||..o{ TA
EA }o..|| U
T ||..o{ EA

Co ||..o{ Re

C ||..o{ Pub 

C ||..o{ G

U ||..o{ GA

GA }o..|| G

Pub  ||..o{ Co
@enduml