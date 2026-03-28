SELECT 
    pl.name                                                         AS producto,
    p.reference                                                     AS ref_modelo,
    pa.reference                                                    AS ref_combinacion,
    MAX(CASE WHEN agl.name = 'Color' THEN al.name END)             AS color,
    MAX(CASE WHEN agl.name != 'Color' THEN al.name END)            AS talla,
    sa.quantity                                                     AS stock,
    ROUND(p.price * 1.19, 0)                                       AS precio_con_iva,
    sa.location                                                     AS ubicacion,
    (
        SELECT CONCAT_WS(' > ',
            COALESCE(cl_ax.name, cl_a2.name),
            cl_bx.name,
            cl_c.name
        )
        FROM ps3vx7_category_product cp2
        JOIN ps3vx7_category c_c
            ON c_c.id_category = cp2.id_category
            AND c_c.id_parent NOT IN (0,1,2)
        JOIN ps3vx7_category_lang cl_c
            ON cl_c.id_category = c_c.id_category AND cl_c.id_lang = 3
        LEFT JOIN ps3vx7_category c_bx
            ON c_bx.id_category = c_c.id_parent
            AND c_bx.id_parent NOT IN (0,1,2)
        LEFT JOIN ps3vx7_category c_ax
            ON c_ax.id_category = c_bx.id_parent
            AND c_ax.id_parent = 2
        LEFT JOIN ps3vx7_category_lang cl_bx
            ON cl_bx.id_category = c_bx.id_category AND cl_bx.id_lang = 3
        LEFT JOIN ps3vx7_category_lang cl_ax
            ON cl_ax.id_category = c_ax.id_category AND cl_ax.id_lang = 3
        LEFT JOIN ps3vx7_category c_a2
            ON c_a2.id_category = c_c.id_parent
            AND c_a2.id_parent = 2
        LEFT JOIN ps3vx7_category_lang cl_a2
            ON cl_a2.id_category = c_a2.id_category AND cl_a2.id_lang = 3
        WHERE cp2.id_product = p.id_product
          AND c_c.id_parent NOT IN (0,1,2)
          AND (c_ax.id_category IS NOT NULL OR c_a2.id_category IS NOT NULL)
        ORDER BY (c_ax.id_category IS NOT NULL) DESC
        LIMIT 1
    ) AS categoria_completa,
    MAX(CASE WHEN fl.name = 'Estaciones'        THEN fvl.value END) AS estaciones,
    MAX(CASE WHEN fl.name = 'Alto de botín'     THEN fvl.value END) AS alto_botin,
    MAX(CASE WHEN fl.name = 'Alto de Botas'     THEN fvl.value END) AS alto_botas,
    MAX(CASE WHEN fl.name = 'Empeine'           THEN fvl.value END) AS empeine,
    MAX(CASE WHEN fl.name = 'Forro interior'    THEN fvl.value END) AS forro_interior,
    MAX(CASE WHEN fl.name = 'Suela'             THEN fvl.value END) AS suela,
    MAX(CASE WHEN fl.name = 'Fabricación'       THEN fvl.value END) AS fabricacion,
    MAX(CASE WHEN fl.name = 'Anatómico'         THEN fvl.value END) AS anatomico,
    MAX(CASE WHEN fl.name = 'Antideslizante'    THEN fvl.value END) AS antideslizante,
    MAX(CASE WHEN fl.name = 'Cierre'            THEN fvl.value END) AS cierre,
    MAX(CASE WHEN fl.name = 'Composición'       THEN fvl.value END) AS composicion,
    MAX(CASE WHEN fl.name = 'Frecuencia de uso' THEN fvl.value END) AS frecuencia_uso,
    MAX(CASE WHEN fl.name = 'Luces leds'        THEN fvl.value END) AS luces_leds,
    MAX(CASE WHEN fl.name = 'Property'          THEN fvl.value END) AS property

FROM ps3vx7_product_attribute pa
JOIN ps3vx7_product p 
    ON pa.id_product = p.id_product
JOIN ps3vx7_product_lang pl 
    ON p.id_product = pl.id_product AND pl.id_lang = 3
JOIN ps3vx7_stock_available sa 
    ON sa.id_product = p.id_product 
    AND sa.id_product_attribute = pa.id_product_attribute
LEFT JOIN ps3vx7_product_attribute_combination pac 
    ON pac.id_product_attribute = pa.id_product_attribute
LEFT JOIN ps3vx7_attribute a 
    ON a.id_attribute = pac.id_attribute
LEFT JOIN ps3vx7_attribute_lang al 
    ON al.id_attribute = a.id_attribute AND al.id_lang = 3
LEFT JOIN ps3vx7_attribute_group_lang agl 
    ON agl.id_attribute_group = a.id_attribute_group AND agl.id_lang = 3
LEFT JOIN ps3vx7_feature_product fp 
    ON fp.id_product = p.id_product
LEFT JOIN ps3vx7_feature_lang fl 
    ON fl.id_feature = fp.id_feature AND fl.id_lang = 3
LEFT JOIN ps3vx7_feature_value_lang fvl 
    ON fvl.id_feature_value = fp.id_feature_value AND fvl.id_lang = 3

GROUP BY 
    pa.id_product_attribute,
    pl.name,
    p.reference,
    pa.reference,
    sa.quantity,
    p.price,
    sa.location

ORDER BY categoria_completa, pl.name, color, talla;
