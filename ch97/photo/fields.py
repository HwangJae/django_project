import os
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile
# class = 상속(python의 상속 개념)
class ThumbnailImageFieldFile(ImageFieldFile):
    def _add_thumb(self, s):
        parts = s.split(".")
        parts.insert(-1, "thumb")
        if parts[-1].lower() not in ['jpeg', 'jpg']:
            parts[-1] = 'jpg'
        return ".".join(parts)
    @property
    def thumb_path(self):
        return self._add_thumb(self.path)


   # 함수지만 속성처럼 사용할때, @property라는 것을 사용한다.
    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    def save(self, name, content, save=True):
        super().save(name, content, save)   # 엄마가 원래 save라는거 다 만들어놨는데, 내가 재정의 할 것이다. 근데 엄마가
                                            # 만든것도 쓰겠다.
                                            # save 코드 -> 원래 큰 이미지 저장 코드
                                            # 아래 코드 -> 썸네일 저장 코드

        img = Image.open(self.path)
        size = (self.field.thumb_width, self.field.thumb_height)
        img.thumbnail(size)
        background = Image.new('RGB',size, (255, 255, 255)) # RGB가 모두 255 이니까 하얀색
        box = (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2))
        background.paste(img, box)
        background.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)

class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile
    # 엄마가 (imagefield)가 이미 정의를 해놨지만, 아들인 썸네일 필드는 자기가 재정의해서 사용하겠다는 뜻.

    # 가로세로 크기를 128로 고정시켰음.
    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs):
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)