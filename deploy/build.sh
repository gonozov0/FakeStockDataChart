docker build -f deploy/base/Dockerfile -t  fake-stock-data-chart/base .
docker build -f deploy/dashboard/Dockerfile -t  fake-stock-data-chart/dashboard .
docker build -f deploy/stock_data_generator/Dockerfile -t  fake-stock-data-chart/stock_data_generator .