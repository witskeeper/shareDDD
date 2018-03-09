<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addInterface" style="margin-top-10">新建接口</i-button>
                <i-button type="success">导入接口</i-button>
            </Col>
        </Row>
        <Row class="margin-top-20">
            <Col span="6">
                <Card>
                    <Tree :data="groupData" style="width:260px"></Tree>
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
    name: 'interface-manage',

    data () {
        return {
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
                                        let query = {interfaceId: params.row.id}
                                        this.$router.push({
                                            name:'interface-edit',
                                            query:query
                                        })
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
                                        this.removeInterfaceData.interfaceId = params.row.id
                                        this.removeInterface()
                                    }
                                }
                            }, '删除')
                        ]);
                    }
                }
            ],
            list:[],
            groupData: [
                {
                    title: '项目名称',
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
                                        width: '40px'
                                    },
                                    on: {
                                        click: () => { this.addGroup() }
                                    }
                                })
                            ])
                        ]);
                    },
                    children: [
                        {
                            title: '父分组',
                            expand: true,
                            children: [
                                {
                                    title: '子分组'
                                }
                            ]
                        }
                    ]
                }
            ],
            removeInterfaceData:{
                interfaceId:""
            },
            addGroupData:{
                parent_groupid:"",
                name:""
            }
        };
    },
    methods: {
        getData () {
            axios.get("/v1/interface/getInterfaceInfosByProject",{params:{projectId:this.$route.query.id,groupId:1,offset:0,limit:10}}
                ).then((res)=>{
                console.log(res)
                console.log(this.projectId)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            }
            )
        },
        getGroupData () {
            axios.get("/v1/group/getGroupInfoByProjectId",{params:{projectId:this.$route.query.id,type:0}}).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.groupData = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        addInterface(){
            this.$router.push({path:"/interface/interface-edit",query:{interfaceId:""}})
        },
        addGroup(){
            this.$Modal.confirm({
                onOk: () => {
                       this.addGroupNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.addGroupData.parent_groupid,
                                autofocus: true,
                                placeholder: '父分组'
                            },
                            on: {
                                input: (val) => {
                                    this.addGroupData.parent_groupid = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.addGroupData.name,
                                autofocus: false,
                                placeholder: '分组名称'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.addGroupData.name = val;
                                }
                            }
                        })
                    ])
                }
            })
        },
        addGroupNet(){

        },
        removeInterface(){
            axios.post("/v1/interface/deleteInterfaceItem",this.removeInterfaceData).then((res)=>{
                console.log(this.removeInterfaceData)
                console.log(res)
                if(res.data.success){
                    this.$Message.success("删除成功");
                    this.getData();
                }else{
                    this.$Message.error("删除数据失败")
                }
            })
        }
    },
    created () {
        this.getData();
    },
};
</script>
