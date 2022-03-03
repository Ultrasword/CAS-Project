package com.engine.hardware;

import com.engine.Camera;
import com.engine.comp.SpriteRenderer;
import com.engine.event.EventHandlerPool;
import com.engine.graphics.Renderer;
import com.engine.graphics.Shader;
import com.engine.graphics.SpriteSheet;
import com.engine.graphics.VBOs.GameEntity2DVBO;
import com.engine.handler.Entities.GameEntity2D;
import com.engine.handler.EntityHandler;
import com.engine.handler.SceneHandler;
import com.engine.handler.Transform2D;
import com.engine.utils.FileHandler;
import com.engine.utils.Time;
import com.war.scene.Lobby;
import org.joml.Vector2f;
import org.joml.Vector3f;
import org.lwjgl.Version;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.*;

import static org.lwjgl.glfw.Callbacks.glfwFreeCallbacks;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.glClear;
import static org.lwjgl.opengl.GL11.GL_COLOR_BUFFER_BIT;
import static org.lwjgl.opengl.GL11.glClearColor;

import static org.lwjgl.opengl.GL30.*;

public class Window {

    private float baseWidth, baseHeight;
    private float width, height;
    private float xratio, yratio;
    private String title;

    private static Window window;
    private long glfwWindow;

    private Window(){
        this.width = 1280;
        this.height = 720;
        this.baseWidth = this.width;
        this.baseHeight = this.height;
        this.xratio = 1f;
        this.yratio = 1f;
        this.title = "War";
    }

    public static Window get(){
        if (window == null)
            window = new Window();
        return window;
    }

    public void init(){
        System.out.println("Starting War with LWJGL version " + Version.getVersion() + "!");
        // set an error printing method
        GLFWErrorCallback.createPrint(System.err).set();

        if (!glfwInit())
            throw new IllegalStateException("Unable to initialize GLFW.");

        // configure
        glfwDefaultWindowHints();
        glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_TRUE);
        glfwWindowHint(GLFW_MAXIMIZED, GLFW_FALSE);

        // create window
        glfwWindow = glfwCreateWindow((int)window.width, (int)window.height, window.title, 0, 0);
        if(glfwWindow == 0)
            throw new IllegalStateException("Failed to create GLFW window.");

        // set the callbacks for hardware
        glfwSetCursorPosCallback(glfwWindow, MouseListener::mousePosCallback);
        glfwSetMouseButtonCallback(glfwWindow, MouseListener::mouseButtonCallback);
        glfwSetScrollCallback(glfwWindow, MouseListener::mouseScrollCallback);
        glfwSetKeyCallback(glfwWindow, KeyListener::keyCallback);

        // this section is scuffed
        glfwSetWindowAspectRatio(glfwWindow, 16, 9);
        glfwSetWindowSizeCallback(glfwWindow, Window::sizeCallback);

        // make opengl context current
        glfwMakeContextCurrent(glfwWindow);
        // vsync?
        glfwSwapInterval(1);

        // make window visible
        glfwShowWindow(glfwWindow);

        // allows opengl context to be used by LWJGL
        GL.createCapabilities();

        // enable some gl options
        glEnable(GL_DEPTH_TEST);
        glDepthFunc(GL_LESS);
    }

    public void loop(){
        Renderer hax = new Renderer();
        EntityHandler entityHandler = new EntityHandler();
        Camera camera = new Camera(width*xratio, height*yratio, new Vector3f(0.0f, 0.0f, -10.0f),
                1.0f, -1f, 100f, 60f);
        camera.adjustOrthoProjection();
        // camera.adjustFrustrumProjection();

        SceneHandler.pushScene(new Lobby());
        SceneHandler.currentScene.setCamera(camera);

        Shader shader = FileHandler.getShader("/shaders/defaultGameEntityVBO");
        GameEntity2DVBO renderer = new GameEntity2DVBO(null);
        renderer.create();

        // spritesheet test
        SpriteSheet spriteSheet = new SpriteSheet("assets/warriorani.png",
                64, 64, 20, 0, 0, 0);
        for(int i = 0; i < 5; i++) {
            for (int j = 0; j < 4; j++){
                GameEntity2D spriteSheetTest = new GameEntity2D(new Transform2D(new Vector3f(i*100 + 25*i, j*100 + 25*j, 0),
                        new Vector2f(100), (i*5 + j)*10f));
                spriteSheetTest.addComponent(new SpriteRenderer(spriteSheet.getSprite(j*5 + i)));
                renderer.addGameEntity2D(spriteSheetTest);
                entityHandler.addGameObject(spriteSheetTest);
            }
        }

        hax.addVBO(renderer);

        // set clear color
        Time.start();
        glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
        while(!glfwWindowShouldClose(glfwWindow)){
            // poll events
            glfwPollEvents();

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

            if (KeyListener.isKeyPressed(GLFW_KEY_A))
                camera.move(-10.f, 0.0f, 0.0f);
            if (KeyListener.isKeyPressed(GLFW_KEY_D))
                camera.move(10.0f, 0.0f, 0.0f);
            if (KeyListener.isKeyPressed(GLFW_KEY_W))
                camera.move(0.0f, 10.0f, 0.0f);
            if (KeyListener.isKeyPressed(GLFW_KEY_S))
                camera.move(0.0f, -10.0f, 0.0f);
            if (KeyListener.isKeyPressed(GLFW_KEY_K))
                renderer.removeGameEntity2D(0);

            camera.update();

            entityHandler.update(Time.deltaTime);
            hax.renderArrays();

            // swap buffers
            glfwSwapBuffers(glfwWindow);
            Time.update();
        }
        hax.clean();
    }

    public void end(){
        FileHandler.close();

        glfwFreeCallbacks(glfwWindow);
        glfwDestroyWindow(glfwWindow);

        glfwTerminate();
        glfwSetErrorCallback(null).free();
    }


    private static void sizeCallback(long window, int w, int h) {
        // get the window
        // window is the window id. should only be useful when there are multiple windows
        Window display = get();
        display.setWidth(w);
        display.setHeight(h);
        glViewport(0, 0, w, h);
        // SceneHandler.currentScene.getCamera().setNewDimensions(w, h);
    }

    public float getWidth() {
        return width;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public float getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public float getMouseX(){
        return MouseListener.getRawX() / this.width * this.baseWidth;
    }

    public float getMouseY(){
        return MouseListener.getRawY() / height * baseHeight;
    }
}
