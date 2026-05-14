from typing import Optional
from .models import Evidence, CrimeEvent


class EslabonEvidencia:
    """
    Representa un eslabón individual en la cadena de custodia de evidencias.
    Implementa protección de datos mediante propiedades privadas.
    """
    def __init__(self, datos_evidencia: Evidence):
        """
        Inicializa el eslabón con datos de evidencia.

        :param datos_evidencia: Objeto Evidence (inmutable).
        """
        self.__datos: Evidence = datos_evidencia
        self.__siguiente: Optional['EslabonEvidencia'] = None

    @property
    def datos(self) -> Evidence:
        """Acceso de lectura a los datos de la evidencia."""
        return self.__datos

    @property
    def siguiente(self) -> Optional['EslabonEvidencia']:
        """Referencia a la siguiente evidencia en el registro."""
        return self.__siguiente

    @siguiente.setter
    def siguiente(self, eslabon: Optional['EslabonEvidencia']) -> None:
        """Establece el siguiente eslabón en el registro."""
        self.__siguiente = eslabon


class HitoCronologico:
    """
    Nodo bidireccional que representa un punto clave en la cronología criminal.
    Permite reconstruir la secuencia de hechos en ambos sentidos temporales.
    """
    def __init__(self, datos_suceso: CrimeEvent):
        """
        Inicializa el hito cronológico.

        :param datos_suceso: Objeto CrimeEvent.
        """
        self.__suceso: CrimeEvent = datos_suceso
        self.__posterior: Optional['HitoCronologico'] = None
        self.__anterior: Optional['HitoCronologico'] = None

    @property
    def suceso(self) -> CrimeEvent:
        """Acceso a los datos del suceso criminal."""
        return self.__suceso

    @property
    def posterior(self) -> Optional['HitoCronologico']:
        """Referencia al suceso ocurrido después en el tiempo."""
        return self.__posterior

    @posterior.setter
    def posterior(self, hito: Optional['HitoCronologico']) -> None:
        self.__posterior = hito

    @property
    def anterior(self) -> Optional['HitoCronologico']:
        """Referencia al suceso ocurrido antes en el tiempo."""
        return self.__anterior

    @anterior.setter
    def anterior(self, hito: Optional['HitoCronologico']) -> None:
        self.__anterior = hito
