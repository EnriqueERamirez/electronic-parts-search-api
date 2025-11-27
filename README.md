# Electronics Parts API

API unificada para búsqueda y comparación de componentes electrónicos en múltiples distribuidores.

## 🚀 Características

- **Búsqueda unificada**: Busca componentes en múltiples distribuidores con una sola consulta
- **Comparación de precios**: Compara el mismo componente en diferentes distribuidores
- **Formato genérico**: Respuestas normalizadas independientes del distribuidor
- **Búsqueda flexible**: Busca en todos los distribuidores o selecciona específicos
- **Búsquedas paralelas**: Consultas simultáneas a múltiples APIs para máxima velocidad
- **Manejo robusto de errores**: Continúa funcionando aunque un distribuidor falle

## 📦 Distribuidores Soportados

- ✅ **DigiKey** - Completamente implementado
- 🔄 **Mouser** - Próximamente
- 🔄 **Farnell** - Próximamente
- 🔄 **LCSC** - Próximamente

## 🏗️ Estructura del Proyecto

```
.
├── main.py                          # Aplicación FastAPI principal
├── config.py                        # Configuración de la aplicación
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Ejemplo de variables de entorno
│
├── models/
│   ├── base.py                      # Modelos genéricos
│   └── digikey.py                   # Modelos específicos de DigiKey
│
├── services/
│   ├── base_service.py              # Interfaz base para servicios
│   ├── aggregator_service.py        # Servicio que agrega múltiples distribuidores
│   ├── digikey_service.py           # Implementación para DigiKey
│   └── auth/
│       └── digikey_auth.py          # Autenticación OAuth2 de DigiKey
│
└── routers/
    ├── components.py                # Endpoints genéricos de componentes
    └── digikey_advanced.py          # Endpoints específicos de DigiKey
```

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd electronics-parts-api
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
# DigiKey
DIGIKEY_CLIENT_ID=tu_client_id
DIGIKEY_CLIENT_SECRET=tu_client_secret
DIGIKEY_USE_SANDBOX=false

# Otros distribuidores (cuando estén implementados)
MOUSER_API_KEY=tu_api_key
FARNELL_API_KEY=tu_api_key
```

### 5. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

## 📖 Documentación de la API

Una vez que la aplicación esté corriendo, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Ejemplos de Uso

### Buscar en todos los distribuidores

```bash
# POST request
curl -X POST "http://localhost:8000/components/search" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "STM32F103",
    "max_results": 20
  }'

# GET request
curl "http://localhost:8000/components/search?keywords=STM32F103&max_results=20"
```

### Buscar en distribuidores específicos

```bash
# POST request
curl -X POST "http://localhost:8000/components/search" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "STM32F103",
    "distributors": ["digikey"],
    "max_results": 20
  }'

# GET request
curl "http://localhost:8000/components/search?keywords=STM32F103&distributors=digikey&max_results=20"
```

### Comparar componente en todos los distribuidores

```bash
curl "http://localhost:8000/components/compare/STM32F103C8T6"
```

### Obtener detalles de un componente específico

```bash
curl "http://localhost:8000/components/digikey/296-6501-1-ND"
```

### Ver distribuidores disponibles

```bash
curl "http://localhost:8000/components/distributors"
```

## 📊 Respuesta de Ejemplo

```json
{
  "components": [
    {
      "distributor": "DigiKey",
      "distributor_part_number": "497-19186-1-ND",
      "manufacturer": "STMicroelectronics",
      "manufacturer_part_number": "STM32F103C8T6",
      "description": "IC MCU 32BIT 64KB FLASH 48LQFP",
      "quantity_available": 2500,
      "minimum_order_quantity": 1,
      "unit_price": 4.18,
      "price_breaks": [
        {
          "quantity": 1,
          "unit_price": 4.18,
          "total_price": 4.18
        },
        {
          "quantity": 10,
          "unit_price": 3.77,
          "total_price": 37.70
        }
      ],
      "datasheet_url": "https://www.st.com/resource/en/datasheet/stm32f103c8.pdf",
      "product_url": "https://www.digikey.com/product-detail/en/-/497-19186-1-ND",
      "image_url": "https://media.digikey.com/Photos/...",
      "parameters": [
        {
          "name": "Core Processor",
          "value": "ARM Cortex-M3"
        },
        {
          "name": "Speed",
          "value": "72MHz"
        }
      ],
      "packaging": "Tray",
      "series": "STM32F1",
      "product_status": "Active",
      "rohs_status": "RoHS Compliant"
    }
  ],
  "total_count": 1,
  "distributors_searched": ["digikey"],
  "search_time_ms": 342.5
}
```

## 🔌 Endpoints Principales

### Endpoints Genéricos de Componentes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/components/distributors` | Lista distribuidores disponibles |
| POST | `/components/search` | Busca componentes (con body JSON) |
| GET | `/components/search` | Busca componentes (con query params) |
| GET | `/components/{distributor}/{part_number}` | Obtiene detalles de un componente |
| GET | `/components/compare/{mpn}` | Compara componente en distribuidores |

### Endpoints Específicos de DigiKey

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/digikey/manufacturers` | Lista de fabricantes |
| GET | `/digikey/categories` | Lista de categorías |
| GET | `/digikey/categories/{id}` | Detalles de categoría |

## 🔐 Autenticación

### DigiKey

1. Regístrate en [DigiKey Developer Portal](https://developer.digikey.com/)
2. Crea una aplicación y obtén:
   - Client ID
   - Client Secret
3. La API maneja automáticamente la autenticación OAuth2

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

## 🛠️ Agregar Nuevos Distribuidores

Para agregar un nuevo distribuidor:

1. **Crear modelos específicos** en `models/{distributor}.py`
2. **Implementar servicio** en `services/{distributor}_service.py`:
   ```python
   class MouserService(BaseDistributorService):
       @property
       def distributor_name(self) -> str:
           return "Mouser"
       
       async def search_components(self, ...):
           # Implementación
       
       async def get_component_details(self, ...):
           # Implementación
   ```
3. **Registrar en aggregator** en `services/aggregator_service.py`:
   ```python
   if self.settings.mouser_api_key:
       self._services[DistributorEnum.MOUSER] = MouserService(self.settings)
   ```
4. **Agregar configuración** en `config.py`
5. **Actualizar enum** en `models/base.py`:
   ```python
   class DistributorEnum(str, Enum):
       DIGIKEY = "digikey"
       MOUSER = "mouser"  # Nuevo
   ```

## 📝 Características del Formato Genérico

Todos los componentes se normalizan al siguiente formato:

```python
class GenericComponent:
    distributor: str                    # Nombre del distribuidor
    distributor_part_number: str        # SKU del distribuidor
    manufacturer: str                   # Fabricante
    manufacturer_part_number: str       # MPN
    description: str                    # Descripción corta
    detailed_description: Optional[str] # Descripción detallada
    quantity_available: int             # Stock disponible
    minimum_order_quantity: int         # MOQ
    unit_price: Optional[float]         # Precio unitario
    price_breaks: List[PriceBreak]      # Escalado de precios
    datasheet_url: Optional[str]        # URL del datasheet
    product_url: Optional[str]          # URL del producto
    image_url: Optional[str]            # URL de imagen
    parameters: List[ComponentParameter]# Especificaciones técnicas
    packaging: Optional[str]            # Tipo de empaque
    series: Optional[str]               # Serie del producto
    product_status: Optional[str]       # Estado (Active, Obsolete, etc)
    rohs_status: Optional[str]          # Cumplimiento RoHS
    raw_data: Dict[str, Any]           # Datos originales del distribuidor
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 📞 Soporte

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/user/repo/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/user/repo/discussions)

## 🗺️ Roadmap

- [x] Integración con DigiKey
- [ ] Integración con Mouser
- [ ] Integración con Farnell/Newark
- [ ] Integración con LCSC
- [ ] Cache de resultados
- [ ] Rate limiting
- [ ] Websockets para búsquedas en tiempo real
- [ ] Export a CSV/Excel
- [ ] Historial de precios
- [ ] Alertas de stock
- [ ] Comparación de especificaciones técnicas

## 🙏 Agradecimientos

- DigiKey por su excelente API
- FastAPI por el framework
- La comunidad de código abierto
