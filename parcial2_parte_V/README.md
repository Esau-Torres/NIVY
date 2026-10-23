# Conocimiento de los expertos – Segundo Parcial de Inteligencia Artificial

**Universidad Modular Abierta – Centro Regional de Santa Ana**
**Asignatura:** Inteligencia Artificial · **Grupo:** "J" · **Catedrático:** Ing. Francisco Javier Morales Ayala

---

## Presentación

En la ingeniería del conocimiento, antes de escribir una sola regla, el ingeniero del conocimiento conversa con el experto del dominio para obtener lo que sabe. A ese proceso se le llama **educción**, y es la etapa más difícil de construir un sistema experto, porque los expertos casi nunca hablan "en reglas": cuentan historias, mezclan experiencias, dan consejos y a veces se desvían del tema.

En este documento encontrará dos entrevistas. **Usted es el ingeniero del conocimiento.** Lea con atención cada conversación y descubra, dentro de lo que cuentan los expertos, qué observan (condiciones) y qué concluyen o recomiendan (conclusiones). No todo lo que dicen sirve para una regla: parte de su trabajo es separar el conocimiento útil de lo que es solo conversación.

Con este documento usted elaborará, para la **Parte IV del parcial**:

- `reglas_computadoras.json`: 5 reglas obtenidas de la entrevista 1.
- `reglas_cafe.json`: 5 reglas obtenidas de la entrevista 2.

> Las personas y negocios de las entrevistas son **ficticios** y fueron creados para este ejercicio. La información técnica se basa en problemas reales y frecuentes.

---

## Entrevista 1 – Reparación de computadoras

**Experto:** Ing. Roberto Menjívar
**Perfil:** ingeniero en sistemas, con 18 años de experiencia. Empezó reparando computadoras en la sala de su casa y hoy tiene su taller, "CompuServicios Menjívar", a dos cuadras del parque Libertad, en Santa Ana. Atiende entre quince y veinte equipos por semana, la mayoría de estudiantes y pequeños negocios.
**Lugar de la entrevista:** el mostrador del taller, un sábado por la mañana, entre cliente y cliente.

---

**—Ingeniero, gracias por recibirnos. ¿Cómo empezó en esto?**

—Pues mire, yo estudié sistemas, pero lo que me gustaba era abrir las máquinas. En la universidad todos mis compañeros me traían sus computadoras, y de ahí se fue haciendo el negocio. Al principio me equivocaba bastante, cambiaba piezas que no había que cambiar. Con los años uno aprende que lo más importante no es saber de piezas, sino saber preguntar. El cliente siempre llega diciendo "ya no sirve", y uno tiene que ir averiguando qué es lo que de verdad le pasa.

**—¿Cuál es el problema que más le llega?**

—El de "no enciende", fácil. Y le voy a contar algo: la mitad de esos casos no es nada. La semana pasada vino una señora angustiada porque su computadora de escritorio no daba ni una luz, ni un ruidito. Le pregunté si había revisado el cable y me dijo que sí. Fui a ver y el cable estaba puesto en la regleta, pero la regleta estaba apagada, porque el nieto la había pisado. Por eso, cuando un equipo está completamente muerto, sin luces y sin ruido de ventiladores, yo siempre empiezo por lo que está afuera: el cable de corriente, el tomacorriente y la regleta.

Ahora, si todo eso está bien conectado y la máquina sigue sin ninguna señal de vida, ahí sí ya me preocupo, porque lo más probable es que se haya arruinado la fuente de poder. Esa es la cajita que recibe la corriente, y no se repara: se cambia. Aquí en Santa Ana pasa bastante después de los apagones, cuando regresa la luz con un pico de voltaje. Por eso yo le digo a la gente que compre un regulador.

**—¿Qué pasa cuando la computadora sí enciende, pero no se ve nada?**

—Ese caso confunde a muchos, porque como la pantalla está oscura creen que la computadora no prendió. Pero uno escucha que los ventiladores sí están girando. Ahí lo primero, aunque parezca tonto, es ver que el monitor esté encendido y que su cable esté bien metido, tanto en el monitor como en la computadora. Usted no se imagina cuántas veces es eso.

Pero hay otra señal que a mí me dice mucho: los pitidos. Si la máquina tiene la pantalla negra y, al encenderla, da unos pitidos, como "piii, piii", eso casi siempre es la memoria RAM, que se movió o tiene los contactos sucios. Yo la saco, le paso un borrador de lápiz por las patitas doradas, la soplo y la vuelvo a poner bien apretada. Nueve de cada diez veces con eso enciende. Si no, ya hay que probar con otra memoria.

**—¿Y las que se apagan solas?**

—Esas me encantan, porque el cliente siempre jura que es virus, y casi nunca es virus. Me cuentan: "trabaja un rato normal y de repente, ¡pum!, se apaga". Entonces yo le toco la parte de atrás a la de escritorio, o la base a la laptop. Si está hirviendo y el ventilador suena como avioneta, ya sé lo que pasa: está llena de polvo por dentro y no puede botar el calor. La computadora se apaga sola para protegerse.

Lo que se hace es abrirla, limpiarle todo el polvo y cambiarle la pasta térmica al procesador, que con los años se seca. Ahora, si el ventilador ni siquiera gira, porque a veces se traba de tanta mugre o se quema, entonces el ventilador ya hay que cambiarlo. Los estudiantes que usan la laptop en la cama, sobre la colcha, son mis mejores clientes en esto, porque tapan las rejillas por donde respira.

**—Muchos estudiantes dicen que su computadora está lenta. ¿Qué les recomienda?**

—Ay, lo de "está lenta" es lo más difícil, porque puede ser de todo. Yo voy descartando. Primero veo cuánto espacio le queda al disco. Si está casi lleno, con fotos, videos y descargas de años, la máquina se pone lentísima. Ahí le digo que borre lo que no usa, que pase sus fotos a una memoria y que desinstale los programas que nunca abre.

Pero si además de lenta le aparecen ventanas de publicidad que nadie abrió, o el navegador se le abre solo en páginas raras, eso ya no es espacio: eso es virus o programas basura que se le metieron por descargar cosas piratas. Ahí hay que pasarle un buen antivirus y limpiar el navegador.

Y hay un tercer caso. Si la computadora es de esas de hace unos siete u ocho años y le pongo el oído y escucho que el disco suena por dentro, como un zumbido que va y viene, es porque tiene disco duro mecánico, de los de antes. A esas yo siempre les recomiendo cambiarlo por un disco de estado sólido, un SSD. No es tan caro y la computadora queda como nueva.

Ojo, que hay un sonido de disco que es diferente y es peligroso. Si el disco hace "clic... clic... clic", como un reloj, repetido, eso significa que se está muriendo. Ahí no hay que esperar: hay que sacar la información importante ya, hacer una copia de seguridad, y cambiar el disco antes de que se pierda todo.

**—¿Y la famosa pantalla azul?**

—La pantalla azul asusta mucho, pero una sola vez no significa nada; a cualquier computadora le puede pasar. Lo que me preocupa es cuando sale seguido. Y casi siempre que me pasa eso, si le pregunto al cliente, me dice: "es que instalé un programa", o "actualicé no sé qué". Entonces lo que hay que hacer es quitar eso que instalaron, o regresar el sistema a como estaba antes, con un punto de restauración.

**—¿Qué hace cuando un cliente dice que no tiene internet?**

—Le hago una sola pregunta: "¿y en su celular sí hay internet?". Esa pregunta me ahorra mucho tiempo. Si me dice que en la casa nadie tiene internet, ni el celular ni la tele, entonces la computadora no tiene la culpa. El problema está en el router o en la compañía. Le digo que desconecte el router, espere un minuto y lo vuelva a conectar; y si sigue igual, que llame a su proveedor.

En cambio, si el celular sí navega bien y solo la computadora no, entonces el problema es de la computadora: reviso que el WiFi esté activado, porque muchas laptops tienen una teclita que lo apaga y la gente la toca sin darse cuenta, o, si es de escritorio, que el cable de red esté bien conectado.

**—¿Algún caso raro que la gente no entienda?**

—Hay uno que me encanta explicar. Gente que me dice: "cada vez que apago la computadora y la vuelvo a encender, la fecha me sale de hace años y la hora está mal". Eso no es virus ni nada del sistema. La tarjeta madre tiene una pilita redonda, como de reloj, que guarda la hora cuando la máquina está apagada. Cuando esa pila se gasta, se olvida de todo. Se cambia la pila, cuesta muy poco, y listo.

Otro caso de laptops: cuando la batería no carga. La gente cree que se arruinó la laptop, pero yo primero veo el cargador. Si la lucecita del cargador no enciende al conectarlo, casi siempre el problema es el cargador, no la computadora. Se prueba con otro cargador y ya se sabe.

**—¿Y algo que sea peligroso?**

—Sí, y esto quiero que lo pongan bien claro. Si una laptop tiene el teclado o el touchpad levantado, como si algo lo empujara desde abajo, o la tapa ya no cierra bien, eso es la batería hinchada. Eso es peligroso, puede incendiarse. Hay que dejar de usarla, no cargarla más y traerla para cambiar la batería.

Y otra cosa: cuando a alguien se le cae café o agua sobre la laptop, lo peor que puede hacer es seguirla usando para "ver si sirve". Lo correcto es apagarla de inmediato, desconectarla, voltearla para que escurra y no encenderla hasta que esté bien seca, por lo menos dos días. Muchas se salvan así.

**—Para terminar, ¿qué consejo le daría a quien va a construir un sistema experto con su conocimiento?**

—Que el sistema pregunte como pregunto yo: de lo más sencillo a lo más complicado. Primero lo de afuera, cables y luces, y después lo de adentro. Y que nunca le diga al cliente que cambie una pieza sin antes descartar lo fácil, porque así es como se pierde la confianza.

---

## Entrevista 2 – Salud del cafeto (hoja y fruto)

**Experta:** Ing. Agr. Marta Linares
**Perfil:** ingeniera agrónoma, con 22 años de experiencia como técnica de campo. Es hija y nieta de caficultores, y ha asesorado a cientos de pequeños productores en las fincas del volcán de Santa Ana, El Congo y la zona de Apaneca.
**Lugar de la entrevista:** el corredor de una finca en las faldas del volcán, después de un recorrido por la plantación.

---

**—Ingeniera, ¿cómo se interesó por el café?**

—Yo crecí entre cafetales. Mi abuelo tenía una fincona aquí arriba y de niña me tocaba ayudar en la corta. Lo que más me llamaba la atención era que mi abuelo, con solo ver una mata, ya sabía si estaba enferma. Yo le preguntaba cómo hacía y me decía: "la hoja le habla a uno, mija". Ya de grande estudié agronomía y entendí que tenía razón: casi todo lo que le pasa a la planta se nota primero en la hoja.

**—Entonces, ¿cómo es una mata sana?**

—Una mata contenta tiene la hoja de un verde bien oscuro, brillante por encima, como si la hubieran encerado, y firme al tocarla. No tiene manchas, no tiene agujeros y no se cae fácil. Cuando yo llego a una finca y veo la mayoría de las hojas así, le digo al productor que va bien y que siga con su mantenimiento normal: su fertilización a tiempo y su limpia de monte. No hay que echarle nada que no necesite, porque eso es gastar dinero.

**—¿Cuál es la enfermedad que más le preocupa?**

—La roya, sin pensarlo. Usted no se imagina lo que fue la roya en los años 2012 y 2013 aquí en El Salvador. Familias enteras perdieron su cosecha. Yo vi fincas que quedaron con las matas peladas, solo los palos.

Para reconocerla hay que voltear la hoja. Por encima usted ve unas manchas amarillentas, como pálidas. Pero lo que la delata es lo de abajo: en el envés de la hoja, justo donde está la mancha, hay un polvillo anaranjado, como polvo de ladrillo, que hasta se le queda en los dedos si lo toca. Cuando hay las dos cosas, la mancha amarilla arriba y ese polvo naranja abajo, no hay duda de que es roya.

Ahí yo le digo al productor que avise al técnico de la cooperativa para que le indique qué control aplicar, porque eso depende de cómo esté la finca. También que regule la sombra, para que entre aire y no se quede tanta humedad. Y, para el futuro, que vaya renovando con variedades resistentes. Si la roya se deja, la mata bota las hojas y la cosecha se pierde.

**—¿Hay manchas que se puedan confundir con la roya?**

—Muchas, y ahí es donde la gente se equivoca. Le voy a contar de dos.

Una es el ojo de gallo. Esas manchas son redonditas, de color café grisáceo, como si alguien hubiera agarrado una perforadora de papel y le hubiera marcado la hoja. A veces el centro de la mancha se seca y se cae, y queda el agujerito. El ojo de gallo es más de las partes altas y frescas, y aparece cuando ha llovido mucho y la finca tiene demasiada sombra, cuando los árboles de sombra están muy cerrados. La recomendación es podar y regular esa sombra para que la mata se ventile y se seque más rápido después de la lluvia.

La otra es la que los productores le dicen mancha de hierro, que es la cercospora. También son manchas redondas, pero color café, con el centro más clarito, casi gris, y un borde amarillo alrededor, como un anillo. Esa es casi lo contrario del ojo de gallo: sale cuando la mata está muy expuesta al sol, sin sombra, y además está mal alimentada, sin su fertilizante. Por eso la recomendación es mejorar la fertilización y darle algo de sombra. Esa también puede atacar los frutos.

**—¿Y si la hoja está amarilla, pero no tiene manchas?**

—¡Esa es la pregunta que yo quería que me hicieran! Mire, hay productores que ven una mata amarilla y ya gritan "¡roya!". Pero no. Si las hojas están amarillas de forma pareja, toda la hoja del mismo tono, sin manchas y sin polvillo, y sobre todo son las hojas de abajo, las más viejas de la rama, eso no es enfermedad. Eso es hambre: le falta nitrógeno. La planta se está comiendo sus propias hojas viejas para alimentar las nuevas. Lo que necesita es fertilización.

Por eso yo siempre digo que hay que voltear la hoja. Si no hay polvo naranja, no es roya.

Y hay otro caso parecido. Cuando lo que se pone feo son las orillas de la hoja, que se ven como quemadas, color café, y la mata está cargada de fruto, eso suele ser falta de potasio. El fruto le está jalando todo. También se corrige con una buena fertilización.

**—Los productores hablan de "un gusanito" que daña la hoja. ¿Qué es?**

—Ese es el minador de la hoja. Es la larva de una palomilla blanquita, chiquitita, que pone sus huevos sobre la hoja. Cuando nace el gusanito, se mete dentro de la hoja, entre la piel de arriba y la de abajo, y se va comiendo la hoja por dentro, como haciendo un túnel.

Por fuera usted ve unas manchas café, de forma irregular, que no son redondas como las de los hongos, sino que parecen caminos o galerías. Si uno levanta con cuidado la telita de la mancha, a veces encuentra el gusanito ahí adentro. Cuando hay esas manchas en forma de caminos y además las hojas se secan y se caen, es minador. Ataca más en el verano, en la época seca, cuando hay poca lluvia. La recomendación es revisar la plantación seguido, contar cuántas hojas dañadas hay y avisar al técnico si son muchas.

**—¿Hay alguna plaga más de la época seca?**

—Sí, la araña roja. No es una araña como la que uno conoce: es un bichito que casi no se ve a simple vista. Lo que se nota es que las hojas pierden el brillo y se ponen de un color como bronceado o rojizo, sobre todo por encima, y eso pasa en el verano, cuando no llueve y hay polvo en los caminos. Si el productor ve sus hojas con ese color bronce en plena época seca, le digo que avise al técnico para revisar con lupa y decidir el control.

**—¿Y en la época de lluvia?**

—En el invierno, cuando llueve muchísimo, hay una que se llama mal de hilachas. Usted la reconoce porque las hojas se secan y se ponen negras o cafés, pero no se caen: se quedan colgando de la rama, agarradas por unos hilitos blancos, como telaraña. Esa se ve más donde hay mucha humedad y sombra. Hay que cortar las ramas afectadas, sacarlas de la finca y regular la sombra.

**—¿Y en el fruto, cuál es el problema más común?**

—La broca, que es la plaga que más plata le quita al productor. Es un escarabajito negro, más chiquito que la cabeza de un alfiler. La hembra se mete al grano de café por la puntita, la coronita del fruto, y adentro pone sus huevos.

Para reconocerla, usted revisa los frutos y ve en la corona un agujerito pequeñito, redondo. Si parte ese fruto y el grano está dañado por dentro, perforado y a veces con un polvillo, es broca. Un fruto con agujerito, pero con el grano sano, puede ser otra cosa; por eso hay que partirlo.

Lo que se recomienda es la buena recolección: recoger los frutos que se caen al suelo y los que quedan en la mata después de la cosecha, lo que aquí le decimos la "repela", porque ahí es donde la broca se esconde y pasa de una cosecha a otra. También se ponen trampas con un atrayente para atraparla.

**—Para terminar, ¿qué consejo le daría a quien va a construir este sistema experto?**

—Que no confunda las manchas. Muchos productores ven algo amarillo y ya creen que es roya, y gastan en productos que no necesitan. Un buen sistema debe preguntar como pregunto yo en el campo: ¿de qué color es?, ¿es redonda o tiene forma de camino?, ¿hay polvo abajo de la hoja?, ¿son las hojas viejas o las nuevas?, ¿está lloviendo o es época seca? Cada detallito cambia el diagnóstico.

---

## Indicaciones para la Parte IV

1. Lea completas las dos entrevistas. No todo lo que dicen los expertos es una regla: separe las anécdotas del conocimiento útil.
2. Para cada regla, identifique qué debe observarse (condiciones) y qué concluye o recomienda el experto (conclusión).
3. Escriba 5 reglas de cada tema en formato JSON, siguiendo la estructura del ejemplo del parcial (`"id"`, `"si"`, `"entonces"`).
4. En cada archivo, al menos 2 reglas deben tener dos o más condiciones.
5. Revise que no tenga reglas repetidas ni contradictorias.
6. Guarde los archivos en la carpeta `parcial2` de su repositorio.