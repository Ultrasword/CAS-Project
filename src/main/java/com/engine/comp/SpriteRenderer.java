package com.engine.comp;

import com.engine.event.DirtyEvent;
import com.engine.event.EventQueue;

public class SpriteRenderer extends Component {

    protected String name = "SpriteRenderer";

    private int texID;
    private boolean dirty;
    private Sprite sprite;

    public SpriteRenderer(Sprite sprite){
        this.sprite = sprite;
        this.texID = sprite.getTexID();
        dirty = true;
    }

    public SpriteRenderer(){
        this.texID = 0;
        dirty = false;
    }

    @Override
    public void update(float dt) {
        // literally nothing to check
    }

    private float[] genTexCoords(){
        return new float[] {1f, 0f, 1f, 1f, 0f, 1f, 0f, 0f};
    }

    public boolean isDirty(){
        return this.dirty;
    }

    public void notDirty(){
        this.dirty = false;
    }

    public float[] getTexCoords() {
        return sprite.getTexCoords();
    }

    public void setTexCoords(float[] texCoords){
        sprite.setTexCoords(texCoords);
    }

    public int getTexID(){
        return this.texID;
    }

    public Sprite getSprite() {
        return sprite;
    }

    public void setTex(Sprite sprite) {
        this.sprite = sprite;
        this.texID = sprite.getTexID();
        dirty = true;
        EventQueue.addEvent(new DirtyEvent(this.getUid(), this.getVboIndex()));
        // TODO - event handler system
        // this should send a entity texture change event - and change the texture :D
    }

    public void setTexID(int id){
        this.texID = id;
        dirty = true;
    }
}
