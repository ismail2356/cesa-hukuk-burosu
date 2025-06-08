-- PostgreSQL veritabanı oluşturma betiği
DROP DATABASE IF EXISTS cesa_hukuk;
CREATE DATABASE cesa_hukuk WITH ENCODING 'UTF8' LC_COLLATE='Turkish_Turkey.1254' LC_CTYPE='Turkish_Turkey.1254' TEMPLATE=template0;
 
-- Veritabanı oluşturuldu, şimdi Django ile migrate yapabilirsiniz. 