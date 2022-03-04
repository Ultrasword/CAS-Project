package com.engine.comp;

import com.engine.handler.SceneHandler;
import com.engine.handler.Transform2D;

public class Testing extends Component{

    private Transform2D transform2D;
    private float rotSpeed = 100;

    public Testing(){
        super();
    }

    public void start(){
        this.transform2D = SceneHandler.currentScene.getEntityHandler().getGameObject(this.uid).getTransform();
    }

    @Override
    public void update(float dt) {
        this.transform2D.addRotation(rotSpeed * dt);
        // this.transform2D.addPosition(rotSpeed * dt, 0, 0);
    }
}
