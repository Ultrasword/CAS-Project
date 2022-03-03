package com.engine.graphics.VBOs;

import com.engine.comp.SpriteRenderer;
import com.engine.graphics.Texture;
import com.engine.handler.Entities.GameEntity2D;
import com.engine.utils.FileHandler;
import org.joml.Math;
import org.joml.Vector2f;
import org.joml.Vector3f;

import static org.lwjgl.opengl.GL13.GL_TEXTURE0;
import static org.lwjgl.opengl.GL13.glActiveTexture;

public class GameEntity2DVBO extends VertexBuffer {

    public final static String defaultShader = "/shaders/defaultGameEntityVBO";
    private int[] texRefs;

    public GameEntity2DVBO(String shaderString) {
        super(true, false, true,
                defaultShader);
        texRefs = new int[9];
        if(shaderString != null) this.setShader(shaderString);
    }

    public void create(){
        // set shader path
        super.create();
        // generate indices
        genIndices();
    }

    @Override
    public void update() {
        // check if dirty
        super.update();
    }

    @Override
    public void bindTextures(){
        // implement binding
        for (int i = 0; i < texSources.size(); i++) {
            glActiveTexture(GL_TEXTURE0 + i + 1);
            texSources.get(i).bind();
        }
        // upload the textures
        shader.uploadIntArray("tex", textures);
    }

    @Override
    public void unbindTextures(){
        // finish unbinding
        for(int i = 0; i < texSources.size(); i++)
            texSources.get(i).unbind();
    }

    public int addGameEntity2D(GameEntity2D entity){
        // check if entity already in a vbo
        if (entity.isInVBO()) return 0;
        if (!hasTexSpace()) return 1;

        entity.setInVBO(true);
        entity.setVBOindex(itemCount);

        Vector3f position = entity.getPosition();
        Vector2f scale = entity.getScale();
        float rot = entity.getRotation();
        // check if entity has a texture
        SpriteRenderer renderer = entity.getComponent(SpriteRenderer.class);
        float[] texCoords = renderer != null ? renderer.getTexCoords() : null;

        int texID = renderer != null ? renderer.getTexID() : 0;
        int inShaderTexID = 0;
        if (renderer != null) {
            addTexture(FileHandler.getTexture(renderer.getSprite().getPath()));
            for (int i = 0; i < texSources.size(); i++) {
                if (texSources.get(i).getTexID() == texID) {
                    textures[i] = texID;
                    inShaderTexID = i;
                    texRefs[i]++;
                    break;
                }
            }
        }

        // rotate the entity and get the points!
        // loop that GameswithGabe made!
        int offset = itemCount * VERTICES_PER_ITEM * VERTEX_OBJECT_SIZE;
        float xAdd = .5f, yAdd = .5f;
        float cos = Math.cos(Math.toRadians(rot)), sin = Math.sin(Math.toRadians(rot));
        // order is bottom right, top left, top right, bottom left
        for (int i = 0; i < VERTICES_PER_ITEM; i++){
            if (i == 1) {
                yAdd = -.5f;
            } else if (i == 2) {
                xAdd = -.5f;
            } else if (i == 3) {
                yAdd = .5f;
            }

            // load position
            float sx = xAdd * scale.x, sy = yAdd * scale.y;
            array[offset] = position.x + (sx*cos - sy*sin);
            array[offset+1] = position.y + (sy*cos + sx*sin);
            array[offset+2] = position.z;

            // if there is a texture, load tex
            if (renderer != null){
                array[offset+3] = texCoords[i*2];
                array[offset+4] = texCoords[i*2+1];
                array[offset+5] = inShaderTexID;
            }else{
                array[offset+3] = 0;
                array[offset+4] = 0;
                array[offset+5] = 0;
            }
            offset += VERTEX_OBJECT_SIZE;
        }

        this.dirty = true;
        itemCount ++;

//        for(int i = 0; i < TEXTURE_BUFFER_SIZE; i++) System.out.print(textures[i]);
        return 2;
    }

    public void addTexture(Texture tex){
        // check if texture already in buffer
        if(!texSources.contains(tex)){
            texSources.add(tex);
        }
    }

    public void removeGameEntity2D(int itemSlot){
        // remove all the data from the itemSlot
        int left = itemSlot * VERTEX_OBJECT_SIZE;
        int right = left + VERTEX_OBJECT_SIZE * 4;
        // you can get the texID directly from the array
        int texID = (int)array[left + VERTEX_OBJECT_SIZE - 1];
        texRefs[texID]--;
        for (int i = left; i < right; i++)
            array[i] = 0;
        this.dirty = true;
    }

}
