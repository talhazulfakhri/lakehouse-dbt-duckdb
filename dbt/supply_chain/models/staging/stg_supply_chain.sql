with raw as (
  select
    product_category,
    sku as product_id,
    try_cast(price as double) as unit_price,
    try_cast(availability as integer) as availability,
    try_cast(number_of_products_sold as integer) as quantity_sold,
    try_cast(revenue_generated as double) as revenue_generated,
    lower(coalesce(customer_demographics,'unknown')) as customer_segment,
    try_cast(stock_levels as integer) as stock_level,
    try_cast(supplier_lead_time_days as integer) as supplier_lead_time_days,
    try_cast(order_quantities as integer) as order_qty,
    try_cast(shipping_times as integer) as shipping_time_days,
    lower(shipping_carrier) as shipping_carrier,
    try_cast(shipping_costs as double) as shipping_cost,
    supplier_name,
    supplier_city,
    try_cast(lead_time_meta as integer) as lead_time_meta,
    try_cast(production_volumes as integer) as production_volume,
    try_cast(manufacturing_lead_time as integer) as mfg_lead_time_days,
    try_cast(manufacturing_costs as double) as manufacturing_cost,
    lower(inspection_results) as inspection_result,
    try_cast(defect_rates as double) as defect_rate,
    lower(transportation_modes) as transport_mode,
    lower(routes) as route,
    try_cast(transport_costs as double) as transport_cost,
    ingest_ts,
    source_file
  from {{ source('raw','raw_supply_chain') }}
)
select * from raw
