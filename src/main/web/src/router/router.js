import Main from '@/views/Main.vue';

// 不作为Main组件的子页面展示的页面单独写，如下
export const loginRouter = {
    path: '/login',
    name: 'login',
    meta: {
        title: 'Login - 登录'
    },
    component: resolve => { require(['@/views/login.vue'], resolve); }
};

export const page404 = {
    path: '/*',
    name: 'error-404',
    meta: {
        title: '404-页面不存在'
    },
    component: resolve => { require(['@/views/error-page/404.vue'], resolve); }
};

export const page403 = {
    path: '/403',
    meta: {
        title: '403-权限不足'
    },
    name: 'error-403',
    component: resolve => { require(['@//views/error-page/403.vue'], resolve); }
};

export const page500 = {
    path: '/500',
    meta: {
        title: '500-服务端错误'
    },
    name: 'error-500',
    component: resolve => { require(['@/views/error-page/500.vue'], resolve); }
};

export const preview = {
    path: '/preview',
    name: 'preview',
    component: resolve => { require(['@/views/form/article-publish/preview.vue'], resolve); }
};

export const locking = {
    path: '/locking',
    name: 'locking',
    component: resolve => { require(['@/views/main-components/lockscreen/components/locking-page.vue'], resolve); }
};

// 作为Main组件的子页面展示但是不在左侧菜单显示的路由写在otherRouter里
export const otherRouter = {
    path: '/',
    name: 'otherRouter',
    redirect: '/home',
    component: Main,
    children: [
        { path: 'home', title: {i18n: 'home'}, name: 'home_index', component: resolve => { require(['@/views/home/home.vue'], resolve); } },
        { path: 'ownspace', title: '个人中心', name: 'ownspace_index', component: resolve => { require(['@/views/own-space/own-space.vue'], resolve); } },
        { path: 'order/:order_id', title: '订单详情', name: 'order-info', component: resolve => { require(['@/views/advanced-router/component/order-info.vue'], resolve); } }, // 用于展示动态路由
        { path: 'shopping', title: '购物详情', name: 'shopping', component: resolve => { require(['@/views/advanced-router/component/shopping-info.vue'], resolve); } }, // 用于展示带参路由
        { path: 'message', title: '消息中心', name: 'message_index', component: resolve => { require(['@/views/message/message.vue'], resolve); } },
        { path: 'interface/interface-info', title: '项目详情', name: 'interface-info', component: resolve => { require(['@/views/interface/interface-info.vue'], resolve); } }

    ]
};

//// 作为Main组件的子页面展示并且在左侧菜单显示的路由写在appRouter里
export const appRouter = [
    {
        path: '/interface',
        icon: 'ios-infinite',
        name: 'interface',
        title: '接口管理',
        component: Main,
        children: [
            {
                path: 'interface-manage',
                title: '项目接口',
                name: 'interface-manage',
                icon: 'link',
                component: resolve => { require(['@/views/interface/interface-manage.vue'], resolve); }
            },
            {
                path: 'project-document',
                title: '项目文档',
                name: 'project-document',
                icon: 'android-send',
                component: resolve => { require(['@/views/interface/project-document.vue'], resolve); }
            }
        ]
    },
    {
        path: '/testcacse',
        icon: 'social-buffer',
        name: 'testcase',
        title: '用例管理',
        component: Main,
        children: [
            {
                path: 'test-collection',
                icon: 'compose',
                name: 'test-collection',
                title: '用例列表',
                component: resolve => { require(['@/views/testcase/test-collection/test-collection.vue'], resolve); }
            },
            {
                path: 'test-suite',
                icon: 'pound',
                name: 'test-suite',
                title: '用例套件',
                component: resolve => { require(['@/views/testcase/test-suite/test-suite.vue'], resolve); }
            }
        ]
    },
    {
        path: '/environment',
        icon: 'arrow-move',
        name: 'environment',
        title: '环境管理',
        component: Main,
        children: [
            {
                path: 'environment-configuration',
                title: '环境配置',
                name: 'environment-configuration',
                icon: 'crop',
                component: resolve => { require(['@/views/environment/environment-configuration.vue'], resolve); }
            },
            {
                path: 'environment-db',
                title: '数据库管理',
                name: 'environment-db',
                icon: 'soup-can',
                component: resolve => { require(['@/views/environment/environment-db.vue'], resolve); }
            }
        ]
    },
    {
        path: '/task',
        icon: 'ios-grid-view',
        name: 'task',
        title: '任务管理',
        component: Main,
        children: [
            {
                path: 'task-timed',
                title: '定时任务',
                name: 'task-timed',
                icon: 'ionic',
                component: resolve => { require(['@/views/task/task-timed/task-timed.vue'], resolve); }
            },
            {
                path: 'task-trigger',
                title: '触发任务',
                name: 'task-trigger',
                icon: 'arrow-shrink',
                component: resolve => { require(['@/views/task/task-trigger/task-trigger.vue'], resolve); }
            }
        ]
    },
    {
        path: '/tools',
        icon: 'settings',
        name: 'tools',
        title: '工具管理',
        component: Main,
        children: [
            {
                path: 'tools-mock',
                title: 'mock工具',
                name: 'tools-mock',
                icon: 'help-buoy',
                component: resolve => { require(['@/views/tools/tools-mock.vue'], resolve); }
            },
            {
                path: 'tools-sign',
                title: 'sign工具',
                name: 'tools-sign',
                icon: 'asterisk',
                component: resolve => { require(['@/views/tools/tools-sign.vue'], resolve); }
            },
            {
                path: 'tools-MD5',
                title: 'MD5加密',
                name: 'tools-MD5',
                icon: 'shuffle',
                component: resolve => { require(['@/views/tools/tools-MD5.vue'], resolve); }
            },
        ]
    },
    {
        path: '/performance',
        icon: 'earth',
        name: 'performance',
        title: '性能监控',
        component: Main,
        children: [
            {
                path: 'performance-monitoring',
                title: '指标监控',
                name: 'performance-monitoring',
                icon: 'ios-monitor',
                component: resolve => { require(['@/views/performance/performance-monitoring/performance-monitoring.vue'], resolve); }
            },
            {
                path: 'performance-test',
                title: '性能测试',
                name: 'performance-test',
                icon: 'ios-flask',
                component: resolve => { require(['@/views/performance/performance-test/performance-test.vue'], resolve); }
            }
        ]
    },
    {
        path: '/analysis',
        icon: 'stats-bars',
        name: 'analysis',
        title: '统计分析',
        component: Main,
        children: [
            {
                path: 'analysis-bug',
                title: 'Bug分析',
                name: 'analysis-bug',
                icon: 'ios-pulse',
                component: resolve => { require(['@/views/analysis/analysis-bug.vue'], resolve); }
            },
            {
                path: 'analysis-case',
                title: 'Case分析',
                name: 'analysis-case',
                icon: 'clipboard',
                component: resolve => { require(['@/views/analysis/analysis-case.vue'], resolve); }
            },
            {
                path: 'analysis-coverage',
                title: '覆盖率分析',
                name: 'analysis-coverage',
                icon: 'ios-pie-outline',
                component: resolve => { require(['@/views/analysis/analysis-coverage.vue'], resolve); }
            }
        ]
    },
    {
        path: '/user',
        icon: 'android-contact',
        name: 'user',
        title: '用户管理',
        component: Main,
        children: [
            {
                path: 'user-list',
                title: '用户列表',
                name: 'user-list',
                icon: 'android-people',
                component: resolve => { require(['@/views/user/user-list.vue'], resolve); }
            },
            {
                path: 'user-authority',
                title: '权限设置',
                name: 'user-authority',
                icon: 'gear-a',
                component: resolve => { require(['@/views/user/user-authority.vue'], resolve); }
            }
        ]
    }
];

// 所有上面定义的路由都要写在下面的routers里
export const routers = [
    loginRouter,
    otherRouter,
    preview,
    locking,
    ...appRouter,
    page500,
    page403,
    page404
];
