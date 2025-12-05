with s as (
  select
    md5(product_id || '-' || cast(ingest_ts as varchar)) as fact_id,
    product_id,
    md5(coalesce(customer_segment,'unknown')) as segment_id,
    coalesce(quantity_sold,0) as quantity_sold,
    coalesce(revenue_generated, quantity_sold * unit_price) as revenue,
    unit_price,
    ingest_ts,
    source_file
  from {{ ref('stg_supply_chain') }}
)
select * from s
