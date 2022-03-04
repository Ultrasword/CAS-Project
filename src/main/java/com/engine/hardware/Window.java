package com.engine.hardware;

import com.engine.handler.SceneHandler;
import com.engine.utils.FileHandler;
import com.engine.utils.Time;
import org.lwjgl.Version;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

import static org.lwjgl.glfw.Callbacks.glfwFreeCallbacks;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL30.GL_DEPTH_BUFFER_BIT;
import static org.lwjgl.opengl.GL30.GL_DEPTH_TEST;
import static org.lwjgl.opengl.GL30.GL_LESS;
import static org.lwjgl.opengl.GL30.glDepthFunc;
import static org.lwjgl.opengl.GL30.glEnable;
import static org.lwjgl.opengl.GL30.glViewport;

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

        // set clear color
        Time.start();
        glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
        while(!glfwWindowShouldClose(glfwWindow)){
            // poll events
            glfwPollEvents();

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

            // update most recent scnee
            SceneHandler.update(Time.deltaTime);
            SceneHandler.render();

            // swap buffers
            glfwSwapBuffers(glfwWindow);
            Time.update();
        }
    }

    public void end(){
        FileHandler.close();

        glfwFreeCallbacks(glfwWindow);
        glfwDestroyWindow(glfwWindow);

        glfwTerminate();
        glfwSetErrorCallback(null).free();
    }

    public float getBaseWidth() {
        return baseWidth;
    }

    public float getBaseHeight() {
        return baseHeight;
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
