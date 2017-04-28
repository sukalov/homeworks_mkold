# homeworks_mkold
**домашние задания в рамках курса "методы компьютерной обработки лингвистических данных"**

### API_project (проект 5)
  В папке лежит 4 изображения. Одно из них, график зависимости длины комментария от длины поста в группе [АКБ](https://vk.com/baneks)по результатам проверки тысячи постов. Отсальные три - по результатам проверки трёхсот постов. Важно отметить, что всилу специфики паблика, длина комментариев там действительно очень зависит от длины поста (больше чем в иных пабликах), и оба графика (*1000_baneks_1.png* и *300_baneks_1.png*) эту зависимость отражают. В папке лежат тексты постов и комментариев (по одному текстовому файлу на пост) (300 постов). И в конце концов сам код. Работает программа очень медленно (300 постов из АКБ обрабатывались несколько часов), но всё же работает. Для проверки программы в другом месте в первой строке функции main() меняем 'baneks' на id паблика, а вместо 300 – любое количество постов. 

### project (проект 1)

  <tr>[ссылка на дерево](https://drive.google.com/drive/folders/0B0WR5yMzU9YzS05QNGYyN0tfRDQ?usp=sharing "ссылка на дерево")

  Программы судорожно доделывались в момент дедлайна, поэтому взаимодействие между ними так и не было настроено, а так же не     было сделано генеральной проверки . Создаётся лишняя папка exem, в которой лежат воспомогательные (промежуточные) файлы, и     эта папка так же не удаляется автоматически.
  
### sql_project (проект 4)

  Небольшие запоздалые коментарии. Программа не справится с такой картиной как пробел+тире+пробел, таким образом тире в тексте не должно окружаться пробелами с двух сторон. И ещё, в программе я забыл убрать дебаг=Тру из последней строчки, надеюсь, последствий это не влечёт, но уточнить всё ж стоит.
