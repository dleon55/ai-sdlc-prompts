# Cómo cambiar el precio de la suscripción

> El precio **cobrado** y el **comunicado** están atados a la misma
> configuración a propósito. No los edites por separado: `terminos.html` y
> `reembolsos.html` derivan del mismo valor que el checkout, así que un
> cambio mal hecho deja documentos legales contradiciendo al sitio — el
> mismo defecto que ya ocurrió con el `$499` de Gumroad.

## Variables

Todas viven en **GitHub → Settings → Secrets and variables → Actions →
Variables** (repositorio, no Environment).

| Variable | Ejemplo | Qué hace |
|---|---|---|
| `PADDLE_PRICE_ID` | `pri_01abc…` | Qué se cobra |
| `PADDLE_PRICE_AMOUNT_USD` | `9` | Qué precio se muestra, en el sitio **y en los documentos legales** |
| `PADDLE_PRICE_ID_ANNUAL` | `pri_01xyz…` | *Opcional.* Plan anual |
| `PADDLE_PRICE_AMOUNT_ANNUAL_USD` | `90` | *Opcional.* Monto anual mostrado |

Las dos anuales se exigen **juntas o ninguna**: un id sin monto pintaría un
botón sin precio, y un monto sin id abriría un checkout vacío. El build
falla si solo pones una.

Si no defines nada, el build usa `1` — el precio vigente. Este mecanismo no
cambia lo que se cobra por accidente.

## Procedimiento para subir el precio

1. **Crea un precio nuevo en Paddle.** No edites el existente: los precios
   ya usados por suscripciones activas no deben mutarse. Catalog →
   Products → *AI-SDLC Pro* → New price.

2. **Los suscriptores actuales no se ven afectados.** Conservan el precio
   con el que se suscribieron mientras no cancelen. Eso cumple la promesa
   de `docs/marketing/early-adopters-program.md` sin trabajo extra.

3. **Actualiza las variables** con el nuevo `pri_` y el nuevo monto. Las
   dos, en el mismo cambio.

4. **Merge a `main`.** El deploy regenera el sitio y los tres documentos
   legales con el precio nuevo, de forma coherente.

5. **Verifica en producción** que `precios.html`, `terminos.html` y
   `reembolsos.html` digan el mismo número.

## El ancla de precio

`PRECIO_LISTA_USD` en `build.py` es el precio tachado ("antes $16 USD").

Se pinta **solo si el precio vigente está por debajo**. Cuando alcancen el
mismo valor, el ancla desaparece sola — mostrar "antes $16" junto a "$16"
se leería como un error, no como una oferta.

## Por qué el plan anual importa

Paddle cobra **5% + $0.50 USD por transacción**. La parte fija es la que
duele en tickets bajos:

| Precio | Comisión | Neto | Margen |
|---|---|---|---|
| $1/mes | $0.55 | $0.45 | 45% |
| $9/mes | $0.95 | $8.05 | 89% |
| $90/año | $5.00 | $85.00 | 94% |

Facturar una vez al año en vez de doce ahorra **11 cargos fijos de $0.50**.
A $1/mes eso casi duplica lo que te queda; a $9/mes ya es marginal.

Paddle mismo lo dice en su página de precios: *"If you're selling products
under $10 […] book a demo for custom pricing"*.
