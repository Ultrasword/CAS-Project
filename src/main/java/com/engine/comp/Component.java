package com.engine.comp;

public abstract class Component {
    protected long uid;
    protected int vboIndex;

    protected String name = "Base";

    public void start(){}

    public abstract void update(float dt);

    public String getName(){
        return name;
    }

    public long getUid() {
        return uid;
    }

    public void setUid(long eid) {
        this.uid = eid;
    }

    public int getVboIndex() {
        return vboIndex;
    }

    public void setVboIndex(int vboIndex) {
        this.vboIndex = vboIndex;
    }
}
