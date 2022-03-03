package com.engine.graphics;

import com.engine.comp.Sprite;
import com.engine.utils.FileHandler;

import java.util.ArrayList;
import java.util.List;

public class SpriteSheet {

    private List<Sprite> sprites;
    private Texture texture;

    public SpriteSheet(String path, int spriteWidth, int spriteHeight, int numSprites, int spacing, int xOff, int yOff) {
        this.sprites = new ArrayList<>();

        this.texture = FileHandler.getTexture(path);
        int currentX = xOff;
        int currentY = texture.getHeight() - spriteHeight - yOff;
        float t, r, l, b;
        float height = (float)texture.getHeight();
        float width = (float)texture.getWidth();
        for(int i = 0; i < numSprites; i++){
            // calculate the tex coords
            t = (currentY + spriteHeight) / height;
            r = (currentX + spriteWidth) / width;
            l = currentX / width;
            b = currentY / height;

            float[] texCoords = {
                    r, b,
                    r, t,
                    l, t,
                    l, b
            };

            Sprite sprite = new Sprite(this.texture.getPath(), texCoords);
            sprite.setSsID(i);
            this.sprites.add(sprite);

            currentX += spriteWidth + spacing;
            if (currentX >= this.texture.getWidth()){
                currentX = xOff;
                currentY -= spriteHeight + spacing;
            }
        }


    }

    public Sprite getSprite(int index){
        return this.sprites.get(index);
    }

}
