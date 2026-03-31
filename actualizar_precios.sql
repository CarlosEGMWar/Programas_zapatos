-- =====================================================
-- RESPALDO (ya ejecutado, no repetir)
-- =====================================================
-- CREATE TABLE IF NOT EXISTS ps3vx7_product_backup_precios AS ...
-- CREATE TABLE IF NOT EXISTS ps3vx7_product_attribute_backup_precios AS ...

-- =====================================================
-- PASO 3: UPDATE MASIVO - AMBAS TABLAS
-- 127 productos unicos
-- =====================================================

-- ref_modelo=1-8 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '1-8';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '1-8';

-- ref_modelo=10 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '10';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '10';

-- ref_modelo=105 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '105';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '105';

-- ref_modelo=106-108 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '106-108';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '106-108';

-- ref_modelo=107 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '107';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '107';

-- ref_modelo=109-113 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '109-113';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '109-113';

-- ref_modelo=11-33-34 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '11-33-34';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '11-33-34';

-- ref_modelo=119 | precio_con_iva=5000 | precio_sin_iva=4201.680672
UPDATE ps3vx7_product SET price = 4201.680672 WHERE reference = '119';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 4201.680672 WHERE p.reference = '119';

-- ref_modelo=12-28-38 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '12-28-38';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '12-28-38';

-- ref_modelo=120 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '120';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '120';

-- ref_modelo=121 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '121';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '121';

-- ref_modelo=122 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '122';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '122';

-- ref_modelo=123 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '123';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '123';

-- ref_modelo=124 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '124';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '124';

-- ref_modelo=125-126 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '125-126';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '125-126';

-- ref_modelo=127-133-154 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '127-133-154';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '127-133-154';

-- ref_modelo=128 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '128';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '128';

-- ref_modelo=129-134-135 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '129-134-135';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '129-134-135';

-- ref_modelo=13-18-32 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '13-18-32';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '13-18-32';

-- ref_modelo=130-137-150-162 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '130-137-150-162';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '130-137-150-162';

-- ref_modelo=131-132 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '131-132';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '131-132';

-- ref_modelo=136 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '136';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '136';

-- ref_modelo=138-144-245 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '138-144-245';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '138-144-245';

-- ref_modelo=139 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '139';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '139';

-- ref_modelo=14-17-37 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '14-17-37';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '14-17-37';

-- ref_modelo=140 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '140';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '140';

-- ref_modelo=141 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '141';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '141';

-- ref_modelo=143-145 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '143-145';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '143-145';

-- ref_modelo=151-152-153-161 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '151-152-153-161';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '151-152-153-161';

-- ref_modelo=167 - 168 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '167 - 168';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '167 - 168';

-- ref_modelo=171 - 173 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '171 - 173';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '171 - 173';

-- ref_modelo=2-7 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '2-7';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '2-7';

-- ref_modelo=203 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '203';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '203';

-- ref_modelo=204-213 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '204-213';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '204-213';

-- ref_modelo=205-211 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '205-211';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '205-211';

-- ref_modelo=206 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '206';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '206';

-- ref_modelo=207 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '207';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '207';

-- ref_modelo=208 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '208';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '208';

-- ref_modelo=209 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '209';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '209';

-- ref_modelo=212 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '212';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '212';

-- ref_modelo=214 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '214';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '214';

-- ref_modelo=215-216 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '215-216';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '215-216';

-- ref_modelo=217 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '217';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '217';

-- ref_modelo=218 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '218';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '218';

-- ref_modelo=219 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '219';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '219';

-- ref_modelo=220 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '220';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '220';

-- ref_modelo=221 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '221';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '221';

-- ref_modelo=222 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '222';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '222';

-- ref_modelo=223 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '223';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '223';

-- ref_modelo=224 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '224';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '224';

-- ref_modelo=225 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '225';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '225';

-- ref_modelo=226 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '226';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '226';

-- ref_modelo=227 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '227';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '227';

-- ref_modelo=228 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '228';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '228';

-- ref_modelo=229 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '229';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '229';

-- ref_modelo=230 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '230';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '230';

-- ref_modelo=231 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '231';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '231';

-- ref_modelo=232 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '232';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '232';

-- ref_modelo=235-262 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '235-262';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '235-262';

-- ref_modelo=236-255 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '236-255';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '236-255';

-- ref_modelo=237 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '237';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '237';

-- ref_modelo=238 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '238';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '238';

-- ref_modelo=239-242 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '239-242';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '239-242';

-- ref_modelo=240 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '240';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '240';

-- ref_modelo=241-261 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '241-261';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '241-261';

-- ref_modelo=243 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '243';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '243';

-- ref_modelo=244 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '244';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '244';

-- ref_modelo=246 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '246';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '246';

-- ref_modelo=247 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '247';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '247';

-- ref_modelo=248-249-250 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '248-249-250';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '248-249-250';

-- ref_modelo=251 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '251';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '251';

-- ref_modelo=252-259 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '252-259';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '252-259';

-- ref_modelo=253-278 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '253-278';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '253-278';

-- ref_modelo=254 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '254';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '254';

-- ref_modelo=256-257-260 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '256-257-260';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '256-257-260';

-- ref_modelo=263-264 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '263-264';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '263-264';

-- ref_modelo=265-266-267 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '265-266-267';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '265-266-267';

-- ref_modelo=268 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '268';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '268';

-- ref_modelo=269 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '269';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '269';

-- ref_modelo=270 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '270';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '270';

-- ref_modelo=271 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '271';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '271';

-- ref_modelo=272-273 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '272-273';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '272-273';

-- ref_modelo=274 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '274';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '274';

-- ref_modelo=275 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '275';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '275';

-- ref_modelo=276 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '276';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '276';

-- ref_modelo=277 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '277';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '277';

-- ref_modelo=279 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '279';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '279';

-- ref_modelo=280 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '280';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '280';

-- ref_modelo=281 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '281';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '281';

-- ref_modelo=282 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '282';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '282';

-- ref_modelo=283 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '283';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '283';

-- ref_modelo=284-285 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '284-285';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '284-285';

-- ref_modelo=286-301 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '286-301';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '286-301';

-- ref_modelo=287-288 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '287-288';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '287-288';

-- ref_modelo=289 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '289';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '289';

-- ref_modelo=290 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '290';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '290';

-- ref_modelo=291 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '291';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '291';

-- ref_modelo=292 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '292';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '292';

-- ref_modelo=293-294-295 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '293-294-295';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '293-294-295';

-- ref_modelo=296-297 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '296-297';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '296-297';

-- ref_modelo=298 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '298';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '298';

-- ref_modelo=299 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '299';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '299';

-- ref_modelo=3-35 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '3-35';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '3-35';

-- ref_modelo=300 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '300';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '300';

-- ref_modelo=302 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '302';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '302';

-- ref_modelo=303 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '303';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '303';

-- ref_modelo=304 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '304';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '304';

-- ref_modelo=46 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '46';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '46';

-- ref_modelo=47-68 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '47-68';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '47-68';

-- ref_modelo=48_60_62 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '48_60_62';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '48_60_62';

-- ref_modelo=49 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '49';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '49';

-- ref_modelo=5-21 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '5-21';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '5-21';

-- ref_modelo=50 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '50';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '50';

-- ref_modelo=51-53-55 | precio_con_iva=10000 | precio_sin_iva=8403.361345
UPDATE ps3vx7_product SET price = 8403.361345 WHERE reference = '51-53-55';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 8403.361345 WHERE p.reference = '51-53-55';

-- ref_modelo=6-26 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '6-26';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '6-26';

-- ref_modelo=86-97 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '86-97';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '86-97';

-- ref_modelo=87-88 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '87-88';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '87-88';

-- ref_modelo=89 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '89';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '89';

-- ref_modelo=9 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '9';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '9';

-- ref_modelo=90-115 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '90-115';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '90-115';

-- ref_modelo=91-110-112 | precio_con_iva=20000 | precio_sin_iva=16806.722689
UPDATE ps3vx7_product SET price = 16806.722689 WHERE reference = '91-110-112';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 16806.722689 WHERE p.reference = '91-110-112';

-- ref_modelo=92-117 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '92-117';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '92-117';

-- ref_modelo=93-94-100 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '93-94-100';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '93-94-100';

-- ref_modelo=95-102-103 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '95-102-103';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '95-102-103';

-- ref_modelo=96-111-116-118 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '96-111-116-118';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '96-111-116-118';

-- ref_modelo=98-101-114 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '98-101-114';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '98-101-114';

-- ref_modelo=99-104 | precio_con_iva=15000 | precio_sin_iva=12605.042017
UPDATE ps3vx7_product SET price = 12605.042017 WHERE reference = '99-104';
UPDATE ps3vx7_product_shop ps JOIN ps3vx7_product p ON p.id_product = ps.id_product SET ps.price = 12605.042017 WHERE p.reference = '99-104';


-- =====================================================
-- ROLLBACK: restaurar precios originales
-- =====================================================
-- UPDATE ps3vx7_product p
--   JOIN ps3vx7_product_backup_precios b ON b.id_product = p.id_product
--   SET p.price = b.price;
--
-- UPDATE ps3vx7_product_shop ps
--   JOIN ps3vx7_product_backup_precios b ON b.id_product = ps.id_product
--   SET ps.price = b.price;