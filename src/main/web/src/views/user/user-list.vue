<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row class="margin-top-20">
            <Col span="18">
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
    name: 'case-list',
    data () {
        return {
            lsitColumns: [
                {
                    title: '名字',
                    key: 'username',
                    render: (h, params) => {
                        return h('div', [
                            h('Icon', {
                                props: {
                                    type: 'person'
                                }
                            }),
                            h('strong', params.row.username)
                        ]);
                    }
                },
                {
                    title: '部门',
                    key: 'department'
                },
                {
                    title: '角色',
                    key: 'role'
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
                            }, '详情'),
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
            list: [
                {
                    username: 'John Brown',
                    department: 18,
                    role: 'New York No. 1 Lake Park'
                }
            ]
        };
    },
    methods: {
        show (index) {
            this.$Modal.info({
                title: 'User Info',

                content: `Name：${this.list[index].username}<br>Age：${this.list[index].department}<br>Address：${this.list[index].role}`
            })
        },
        remove (index) {
            this.list.splice(index, 1);
        },
        getData (group_id) {
            axios.get("/v1/case/getCaseInfosByCondition",{params:{projectId:this.$route.query.projectId,groupId:group_id,offset:0,limit:10}}
                ).then((res)=>{
                console.log(res)
                console.log(this.$route.query.projectId)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },
        removeGroup(root,node,data){
            alert(JSON.stringify(root));
            alert(JSON.stringify(node));
            axios.post("/v1/group/deleteGroup",data).then((res)=>{
                console.log(data);
                console.log(res);
                if(res.data.success){
                    this.$Message.success("删除成功");
                    const parentKey = root.find(el => el === node).parent;
                    const parent = root.find(el => el.nodeKey === parentKey).node;
                    const index = parent.children.indexOf(data);
                    parent.children.splice(index, 1);
                    this.getGroupData();
                }else{
                    this.$Message.error("删除数据失败");
                }
            });
        }
    },
    created () {

    },
}
</script>
