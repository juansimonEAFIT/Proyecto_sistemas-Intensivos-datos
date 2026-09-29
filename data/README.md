# data/

Datasets descargados para simular las fuentes de TiendaCol. **No se suben a git** (ver `.gitignore`): solo se versionan este archivo y `sample/`.

| Dataset | Enlace | Carpeta sugerida |
|---|---|---|
| Olist (órdenes, pagos, catálogo, clientes, vendedores) | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce | `data/olist/` |
| REES46 multi-categoría (clickstream) | https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store | `data/rees46/` |
| REES46 cosméticos (clickstream, alternativa liviana) | https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop | `data/rees46/` |

## Descarga

Requiere una cuenta de Kaggle y su token de API (`KAGGLE_USERNAME` y `KAGGLE_KEY` en `.env`, o `~/.kaggle/kaggle.json`).

```bash
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/olist --unzip
kaggle datasets download -d mkechinov/ecommerce-behavior-data-from-multi-category-store -p data/rees46 --unzip
```

El tamaño, la licencia y lo que les falta a los datasets frente a TiendaCol están en `CLAUDE.md`, §8.
