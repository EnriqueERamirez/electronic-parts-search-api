# 🚀 Guía de Inicio Rápido

## Instalación y Configuración en 5 Pasos

### 1️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar variables de entorno

Copia el archivo de ejemplo y edítalo con tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` y agrega tus credenciales de DigiKey:

```env
DIGIKEY_CLIENT_ID=tu_client_id_aqui
DIGIKEY_CLIENT_SECRET=tu_client_secret_aqui
```

### 3️⃣ Probar la configuración

```bash
python test_setup.py test
```

Si todo está correcto, verás:
```
✓ Todos los tests pasaron exitosamente!
```

### 4️⃣ Iniciar el servidor

```bash
uvicorn main:app --reload
```

### 5️⃣ Explorar la API

Abre tu navegador en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Ejemplos Rápidos

### Buscar componentes en todos los distribuidores

**Usando curl:**
```bash
curl "http://localhost:8000/components/search?keywords=STM32F103"
```

**Usando Python:**
```python
import requests

response = requests.get(
    "http://localhost:8000/components/search",
    params={"keywords": "STM32F103"}
)
components = response.json()
print(f"Encontrados: {components['total_count']} componentes")
```

**Usando JavaScript:**
```javascript
fetch('http://localhost:8000/components/search?keywords=STM32F103')
  .then(response => response.json())
  .then(data => console.log(`Encontrados: ${data.total_count} componentes`));
```

### Buscar en distribuidores específicos

```bash
curl "http://localhost:8000/components/search?keywords=resistor&distributors=digikey"
```

### Comparar precios de un componente

```bash
curl "http://localhost:8000/components/compare/STM32F103C8T6"
```

### Obtener detalles de un componente

```bash
curl "http://localhost:8000/components/digikey/296-6501-1-ND"
```

## 📊 Estructura de Respuesta

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
      "unit_price": 4.18,
      "price_breaks": [
        {"quantity": 1, "unit_price": 4.18, "total_price": 4.18},
        {"quantity": 10, "unit_price": 3.77, "total_price": 37.70}
      ],
      "datasheet_url": "https://...",
      "product_url": "https://...",
      "parameters": [
        {"name": "Core Processor", "value": "ARM Cortex-M3"},
        {"name": "Speed", "value": "72MHz"}
      ]
    }
  ],
  "total_count": 1,
  "distributors_searched": ["digikey"],
  "search_time_ms": 342.5
}
```

## 🔑 Obtener Credenciales de DigiKey

1. Ve a [DigiKey Developer Portal](https://developer.digikey.com/)
2. Crea una cuenta o inicia sesión
3. Crea una nueva aplicación:
   - Production API o Sandbox API
   - Obtén tu Client ID y Client Secret
4. Copia las credenciales a tu archivo `.env`

## ❓ Solución de Problemas

### Error: "DigiKey service is not configured"

**Problema:** Las credenciales no están configuradas.

**Solución:**
1. Verifica que el archivo `.env` existe
2. Verifica que `DIGIKEY_CLIENT_ID` y `DIGIKEY_CLIENT_SECRET` están configurados
3. Reinicia el servidor

### Error: "401 Unauthorized"

**Problema:** Las credenciales son incorrectas.

**Solución:**
1. Verifica que las credenciales en `.env` sean correctas
2. Verifica que estás usando las credenciales correctas (Production vs Sandbox)
3. Si usas Sandbox, configura `DIGIKEY_USE_SANDBOX=true`

### Error de conexión

**Problema:** No se puede conectar a la API de DigiKey.

**Solución:**
1. Verifica tu conexión a internet
2. Verifica que las URLs de API sean correctas
3. Intenta con Sandbox: `DIGIKEY_USE_SANDBOX=true`

## 📚 Recursos Adicionales

- [Documentación completa](README.md)
- [DigiKey API Documentation](https://developer.digikey.com/documentation)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🆘 Obtener Ayuda

Si tienes problemas:

1. Ejecuta el diagnóstico: `python test_setup.py info`
2. Revisa los logs del servidor
3. Abre un issue en GitHub con:
   - Mensaje de error completo
   - Salida de `python test_setup.py info` (sin credenciales)
   - Pasos para reproducir el problema

## ✅ Checklist de Verificación

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado con credenciales
- [ ] Test de conexión pasado (`python test_setup.py test`)
- [ ] Servidor iniciado (`uvicorn main:app --reload`)
- [ ] Documentación accesible (http://localhost:8000/docs)
- [ ] Primera búsqueda exitosa

¡Felicidades! 🎉 Ya estás listo para usar la API.
