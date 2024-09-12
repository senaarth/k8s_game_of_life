from elasticsearch import Elasticsearch
# PASSWORD=$(kubectl get secret database-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)
es = Elasticsearch(
    "https://database-es-http:9200",
    basic_auth=("elastic", "ID60n32o2Par4Gfx9CTOa623"),
    verify_certs=False,
    ssl_show_warn=False,
)

def parse_metrics(metrics_string, engine):
    parsed_metrics = {
        "engine": engine,
    }

    for metric in metrics_string.split(","):
        key, value = metric.split("=")
        parsed_metrics[key] = value

    return parsed_metrics

def send_metrics_to_elastic(metrics, engine):
    try:
        parsed_metrics = parse_metrics(metrics, engine)
        es.index(index="engines-perfomance-metrics", document=parsed_metrics)
    except Exception as e:
        print(f"Erro no elasticsearch: {e}")
