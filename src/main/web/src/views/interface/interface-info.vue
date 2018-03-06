<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addInterface" style="margin-top-10">新增接口</i-button>
                <i-button type="success">导入接口</i-button>
            </Col>
        </Row>
        <Row class="margin-top-20">
            <Col span="6">
                <Card>
                    <Tree :data="groupData" :render="renderContent" style="width:260px"></Tree>
                </Card>
            </Col>
            <Col span="18" class="padding-left-10">
                <Card>
                    <div >
                        <Table border :columns="lsitColumns" :data="list" ></Table>
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
    import axios  from 'axios';
    export default {
        name: 'interface-info',
        data () {
            return {
                groupData: [
                    {
                        title: "parents",
                        expand: true,
                        render: (h, { root, node, data }) => {
                            return h('span', {
                                style: {
                                    display: 'inline-block',
                                    width: '100%'
                                }
                            }, [
                                h('span', [
                                    h('Icon', {
                                        props: {
                                            type: 'ios-folder-outline'
                                        },
                                        style: {
                                            marginRight: '8px'
                                        }
                                    }),
                                    h('span', data.title)
                                ]),
                                h('span', {
                                    style: {
                                        display: 'inline-block',
                                        float: 'right',
                                        marginRight: '32px'
                                    }
                                }, [
                                    h('Button', {
                                        props: Object.assign({}, this.buttonProps, {
                                            icon: 'ios-plus-empty',
                                            type: 'primary'
                                        }),
                                        style: {
                                            width: '52px'
                                        },
                                        on: {
                                            click: () => { this.append(data) }
                                        }
                                    })
                                ])
                            ]);
                        },
                        children: [
                            {
                                title: 'child 1-1',
                                expand: true,
                                children: [
                                    {
                                        title: 'leaf 1-1-1',
                                        expand: true
                                    }
                                ]
                            }
                        ]
                    }
                ],
                buttonProps: {
                    type: 'ghost',
                    size: 'small',
                },
                lsitColumns: [
                    {
                        title: '接口Id',
                        key: 'id'
                    },
                    {
                        title: '接口名称',
                        key: 'name'
                    },
                    {
                        title: '接口地址',
                        key: 'url'
                    },
                    {
                        title: '编辑时间',
                        key: 'gmt_modify'
                    },
                    {
                        title: '编辑人',
                        key: 'create_username'
                    },
                    {
                        title: '操作',
                        key: 'action',
                        width: 150,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.show(params.index)
                                        }
                                    }
                                }, '编辑'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.remove(params.index)
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
                ],
                list:[],
                getInterfaceListData:{
                    projectId:"",
                    groupId:"",
                    offset:"10",
                    limit:"1"
                }
            }
        },
        methods: {
            renderContent (h, { root, node, data }) {
                return h('span', {
                    style: {
                        display: 'inline-block',
                        width: '100%'
                    }
                }, [
                    h('span', [
                        h('Icon', {
                            props: {
                                type: 'ios-paper-outline'
                            },
                            style: {
                                marginRight: '8px'
                            }
                        }),
                        h('span', data.title)
                    ]),
                    h('span', {
                        style: {
                            display: 'inline-block',
                            float: 'right',
                            marginRight: '32px'
                        }
                    }, [
                        h('Button', {
                            props: Object.assign({}, this.buttonProps, {
                                icon: 'ios-plus-empty'
                            }),
                            style: {
                                marginRight: '8px'
                            },
                            on: {
                                click: () => { this.append(data) }
                            }
                        }),
                        h('Button', {
                            props: Object.assign({}, this.buttonProps, {
                                icon: 'ios-minus-empty'
                            }),
                            on: {
                                click: () => { this.remove(root, node, data) }
                            }
                        }),
                        h('Button', {
                            props: {
                                type: 'text',
                                icon: 'edit'
                            },
                            on: {
                                click: (event) => {
                                    this.data = true;
                                    this.data = JSON.parse(JSON.stringify(this.data));
                                }
                            }
                        })
                    ])
                ]);
            },
            append (data) {
                const children = data.children || [];
                children.push({
                    title: 'appended node',
                    expand: true
                });
                this.$set(data, 'children', children);
            },
            remove (root, node, data) {
                const parentKey = root.find(el => el === node).parent;
                const parent = root.find(el => el.nodeKey === parentKey).node;
                const index = parent.children.indexOf(data);
                parent.children.splice(index, 1);
            },
//            groupData () {
//                axios.get("/v1/group/getGroupInfoByProjectId").then((res)=>{
//                console.log(res)
//                if(res.data.success){
//                    this.list = res.data.message;
//                }else{
//                    this.$Message.error("获取数据失败")
//                }
//            })
//            },
            getData () {
                axios.get("/v1/interface/getInterfaceInfosByProject",this.getInterfaceListData).then((res)=>{
                console.log(this.getInterfaceListData)
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
            },
            addInterface(index){
                this.$router.push({path:"/interface/interface-edit",query:{interfaceId:""}})
            },
            onRowClick(rowData,index){
                console.log(rowData)
                this.$router.push({path:"/interface/interface-edit",query:{interfaceId:rowData.id}})
            },
        }
    }
</script>
