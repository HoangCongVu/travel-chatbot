`` truy cap docker
docker ps
docker exec -it 47f91c5c760f bash
psql -U clinic-website-chatbot -d clinic-website-chatbot

##lenh xoa table:

DO

$$
DECLARE
    r RECORD;
BEGIN
    -- Lặp qua tất cả các bảng trong schema 'public'
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END;
$$;


lenh insert table de test
insert into tour_types(id, type_name)
values(1, 'tour du lich');



tạo api chatbot api/chatbot
input : chatid, message,
output : 1 doan text trả lời


list port lsof -i :8000
kill port kill -9 PID


$$
