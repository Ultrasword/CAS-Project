package com.engine.handler;

import com.engine.comp.Component;
import com.engine.event.DirtyEvent;
import com.engine.event.EventQueue;
import org.joml.Vector3f;

import java.util.HashMap;

public class GameObject {

    public static long id = 0;

    protected Transform2D transform;
    protected HashMap<String, Component> components;
    private boolean inVBO, dirty, dead;
    private int VBOindex, inVertexPosition;
    private long uid;

    public GameObject(){
        this.inVBO = false;
        this.dead = false;
        this.components = new HashMap<>();
        this.uid = getID();
        this.transform = new Transform2D();
    }

    public Transform2D getTransform() {
        return transform;
    }

    public void setTransform(Transform2D transform) {
        this.transform = transform;
    }

    public void update(float dt){}

    protected void updateComponents(float dt){
        for(String comp : components.keySet()){
            components.get(comp).update(dt);
        }
    }

    public <T extends Component> T getComponent(Class<T> componentClass){
        if (components.containsKey(componentClass.getName())){
            return componentClass.cast(components.get(componentClass.getName()));
        }else return null;
    }

    public <T extends Component> void removeComponent(Class<T> componentClass){
        components.remove(componentClass.getName());
    }

    public <T extends Component> void addComponent(T component){
        component.setUid(this.getUID());
        component.setVboIndex(this.getVBOindex());
        components.put(component.getClass().getName(), component);
    }

    public void start(){
        this.transform.setGameObject(this);
        for(Component component : this.components.values()){
            component.start();
        }
    }

    public void checkIfDirty(){
        if(this.inVBO && this.dirty) {
            SceneHandler.currentScene.getRenderer().getVboArray().get(getVBOindex()).addDirtySprite(this);
//            EventQueue.addEvent(new DirtyEvent(this.getUID(), this.getVBOindex()));
            dirty = false;
        }
    }

    protected boolean isDirty(){
        return this.dirty;
    }

    protected void notDirty(){
        this.dirty = false;
    }

    protected void setDirty(){
        this.dirty = true;
    }

    public boolean isInVBO(){
        return this.inVBO;
    }

    public void setInVBO(boolean is){
        inVBO = is;
    }

    public void setVBOindex(int i){
        this.VBOindex = i;
        for(Component component : this.components.values()){
            component.setUid(this.getUID());
            component.setVboIndex(this.getVBOindex());
        }
    }

    public int getVBOindex(){
        return this.VBOindex;
    }

    public static long getID(){
        return id++;
    }

    public long getUID(){
        return this.uid;
    }

    public int getInVertexPosition() {
        return inVertexPosition;
    }

    public void setInVertexPosition(int inVertexPosition) {
        this.inVertexPosition = inVertexPosition;
    }

    public boolean isDead() {
        return dead;
    }

    public void setDead(boolean dead) {
        this.dead = dead;
    }
}
