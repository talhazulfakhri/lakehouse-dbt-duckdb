with s as (
  select distinct product_id, product_category, unit_price
  from {{ ref('stg_supply_chain') }}
)
select
  product_id,
  product_category,
  unit_price
from s
where product_id is not null
