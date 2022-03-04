package com.engine.graphics.VBOs;

import com.engine.graphics.Texture;
import com.engine.graphics.UI.UICamera;
import com.engine.graphics.UI.UIObject;
import com.engine.handler.GameObject;
import com.engine.handler.Transform2D;
import com.engine.utils.Time;
import org.joml.Math;
import org.joml.Vector2f;
import org.joml.Vector3f;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL13.GL_TEXTURE0;
import static org.lwjgl.opengl.GL13.glActiveTexture;

public class UIVBO extends VertexBuffer {
    public final static String defaultShader = "/shaders/defaultUI";

    private UICamera uiCamera;

    public UIVBO(String shaderPath, UICamera uiCamera) {
        super(true, false, true, defaultShader);
        if(shaderPath != null) this.setShader(shaderPath);
        this.uiCamera = uiCamera;
    }

    public void create(){
        // set shader path
        super.create();
        // generate indices
        genIndices();
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

    @Override
    public <T extends GameObject> void calculateVertices(T gameObject) {
        UIObject object = (UIObject) gameObject;
        // get the transform and the texture from the object
        int texID = object.getTexID();
        Transform2D transform2D = object.getTransform2D();
        Vector3f pos = transform2D.getPosition();
        Vector2f scale = transform2D.getScale();
        float rot = transform2D.getRotation();
        Texture texture = object.getTexture();
        object.setInVBO(true);

        int inShaderTexID = 0;
        // add texture
        if(!texSources.contains(texture)) texSources.add(texture);
        for (int i = 0; i < texSources.size(); i++) {
            if (texSources.get(i).getTexID() == texID) {
                inShaderTexID = i + 1;
                break;
            }
        }
        // now we load everything
        // loop through :O
        int offset = itemCount * VERTICES_PER_ITEM * VERTEX_OBJECT_SIZE;
        float xAdd = 1.f, yAdd = 1.f;
        float cos = Math.cos(Math.toRadians(rot)), sin = Math.sin(Math.toRadians(rot));
        // order is bottom right, top left, top right, bottom left
        for (int i = 0; i < VERTICES_PER_ITEM; i++){
            if (i == 1) {
                yAdd = 0.0f;
            } else if (i == 2) {
                xAdd = 0.0f;
            } else if (i == 3) {
                yAdd = 1.0f;
            }

            // load position
            float sx = xAdd * scale.x, sy = yAdd * scale.y;
            array[offset] = pos.x + (sx*cos - sy*sin);
            array[offset+1] = pos.y + (sy*cos + sx*sin);
            array[offset+2] = pos.z;

            // if there is a texture, load tex
            array[offset+3] = UIObject.texCoords[i*2];
            array[offset+4] = UIObject.texCoords[i*2+1];
            array[offset+5] = inShaderTexID;

            offset += VERTEX_OBJECT_SIZE;
        }

        this.dirty = true;
    }

    @Override
    public <T extends GameObject> int addGameObject(T gameObject) {
        if (!(gameObject instanceof UIObject)) return 0;
        return this.addUIObject(((UIObject) gameObject));
    }

    public int addUIObject(UIObject object){
        // check if has space
        if(object.isInVBO()) return 0;
        // check if its texture is in the buffer already
        if(!hasTexSpace()) return 0;

        itemCount ++;

        return 1;
    }

    @Override
    public void howToRender() {
        glDisable(GL_DEPTH_FUNC);
        shader.uploadFloat("uTime", Time.getTime());
        shader.uploadMat4f("proj", this.uiCamera.getProjMatrix());

        // render
        bindShader();
        bindTextures();
        render();
        unbindTextures();
        unbindShader();
        glEnable(GL_DEPTH_FUNC);
    }

}
