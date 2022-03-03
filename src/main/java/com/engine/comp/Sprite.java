package com.engine.comp;

import com.engine.graphics.Texture;
import com.engine.utils.FileHandler;

public class Sprite extends Component{

    private String path;
    private float[] texCoords;
    private int ssID;
    private int texID;

    public Sprite(String path, float[] texCoords){
        this.path = path;
        this.texID = FileHandler.getTexture(path).getTexID();
        this.texCoords = texCoords;
        this.ssID = 0;
    }

    public Sprite(String path){
        this.path = path;
        this.texID = FileHandler.getTexture(path).getTexID();
        this.texCoords = genTexCoords();
        this.ssID = 0;
    }

    public Sprite(Texture tex){
        // load the texture ig
        this.path = tex.getPath();
        this.texCoords = genTexCoords();
        this.texID = tex.getTexID();
        this.ssID = 0;
    }

    @Override
    public void update(float dt) {
        // nothing
    }

    private float[] genTexCoords(){
        //                  br      tr      tl      bl
        return new float[] {1f, 0f, 1f, 1f, 0f, 1f, 0f, 0f};
    }

    public float[] getTexCoords() {
        return texCoords;
    }

    public void setTexCoords(float[] texCoords) {
        this.texCoords = texCoords;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public int getSsID() {
        return ssID;
    }

    public void setSsID(int ssID) {
        this.ssID = ssID;
    }

    public int getTexID() {
        return texID;
    }

    public void setTexID(int texID) {
        this.texID = texID;
    }
}
