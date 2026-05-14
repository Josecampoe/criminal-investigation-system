# Sistema de Investigación Criminal

Un sistema robusto y modular desarrollado en Python para la gestión de evidencias y eventos criminales, utilizando estructuras de datos avanzadas (Listas Enlazadas Simples y Dobles) para garantizar la integridad y el orden cronológico de las investigaciones.

## Características

- **Gestión de Evidencias**: Utiliza una Lista Enlazada Simple para el almacenamiento eficiente de evidencias forenses inmutables.
- **Cronología Criminal**: Implementa una Lista Doblemente Enlazada para navegar bidireccionalmente por la línea de tiempo de un crimen.
- **Persistencia**: Capacidad de guardar y cargar datos en formato JSON para mantener la continuidad de las investigaciones.
- **Búsqueda Avanzada**: Filtros por agente recolector, ubicación, tipo de evidencia y más.
- **Integridad**: Encapsulamiento estricto de datos mediante propiedades y nodos privados.

## Requisitos

- Python 3.7+ (utiliza `dataclasses`)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Josecampoe/criminal-investigation-system.git
   cd criminal-investigation-system
   ```

2. (Opcional) Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

## Uso

Para ejecutar la aplicación principal e interactuar con el sistema:

```bash
python FinalCriminalSystem/main.py
```

## Pruebas

Para ejecutar la suite de pruebas unitarias:

```bash
python -m unittest discover tests
```

## Estructura del Proyecto

- `FinalCriminalSystem/`: Paquete principal con la lógica del sistema.
- `tests/`: Suite de pruebas unitarias.
- `data/`: Directorio sugerido para la persistencia de datos JSON.
