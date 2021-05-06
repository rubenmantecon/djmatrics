/* Contexto
Matrícula externa: alumno externo al centro
Matrícula interna: matrícula de un alumno que ya se ha matriculado en el centro, y se vuelve a matricular (porque pasa de primero a segundo, o repite curso)
Fraccionada: pagada en dos tiempos
Parcial: que no se matricula de todo el curso, si no de UFs sueltas.
Las exenciones se aplican sólo al precio público de los CFGS, que son 360e aprox
Se preferirá siempre la exención más alta
Sólo aplica una excención del 50%. No son acumulables.

*/

function computePrice(params) {
	seguro = 1.12;
	material = 0;
	AMPA = 15;
	UF = 25;
	over28;
	matrículaExterna;
	matrículaInterna;
	finalPrice = 0;

	if (over28) {
		seguro = 20;
	}
	if (CFGM) {
		if ("Matrícula externa") {
			material = 70.38;
			finalPrice = seguro + AMPA + material;
		}
		else if ("Matrícula interna") {
			if ("Sólo tiene las FCT pendientes") {
				material = 10;
				finalPrice = material + seguro + AMPA;
			} else {
				material = 35.38;
				finalPrice = material + seguro + AMPA;
			}
		}
	}
	else if (CFGS) {
		if ("Matrícula externa") {
			if ("Total") {
				if ("Exención del 100%"){
					precioPublico = 0;
					//No es posible fraccionar el pago
					finalPrice = material + seguro;
				}
				else if ("Exención del 50%") {
					precioPublico/2;
					if ("Fraccionada en dos tiempos") {
						precioPublico/2; //Sí, otra vez
						firstPayment = material + seguro + precioPublico;
						secondPayment = precioPublico;
	
					} else if ("Pago de una sola vez") {
						finalPrice = precioPublico;
					}

				}
			}
			else if ("Parcial") {
				//Caso raro que aún me tienen que concretar
			}
		} else if ("Matrícula interna") {
			if ("Parcial (la mayoría de los casos)") {
				//El precio máximo a pagar es del precio público
				if ("La cantidad") {
					
				}
				
			} else if ("Total (repite todo el curso)") {

			}
		}
	}
}
