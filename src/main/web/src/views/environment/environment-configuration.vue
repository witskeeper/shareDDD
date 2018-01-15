<style lang="less">
    @import './environment-configuration.less';
</style>

<template>
    <div>
        <Row>
            <Card>
                <p slot="title">
                    <Icon type="ios-list"></Icon>
                    环境列表
                </p>
                <Row type="flex" justify="center" align="middle" class="advanced-router">
                    <Table :columns="shoppingColumns" :data="shoppingData" style="width: 100%;"></Table>
                </Row>
            </Card>
        </Row>
    </div>
</template>

<script>
export default {
    name: 'argument-page',
    data () {
        return {
            shoppingColumns: [
                {
                    type: 'index',
                    title: '序号',
                    width: 60
                },
                {
                    title: '环境名称',
                    key: 'name',
                    align: 'center'
                },
                {
                    title: '编辑人',
                    key: 'edit_user',
                    align: 'center'
                },
                {
                    title: '编辑时间',
                    key: 'time'
                },
                {
                    title: '操作',
                    key: 'option',
                    align: 'center',
                    render: (h, params) => {
                        return h('Button', {
                            props: {
                                type: 'text',
                                size: 'small'
                            },
                            on: {
                                click: () => {
                                    let query = {name: params.row.name};
                                    this.$router.push({
                                        name: 'name',
                                        query: query
                                    });
                                }
                            }
                        }, '编辑');
                    }
                }
            ],
            shoppingData: [
                {
                    edit_user: 100001,
                    name: 'ERP测试环境新库',
                    time: '2017年11月12日'
                },
                {
                    edit_user: 100002,
                    name: 'ERP测试环境老库',
                    time: '2017年11月5日'
                },
                {
                    edit_user: 100003,
                    name: 'SCP测试环境',
                    time: '2017年11月8日'
                },
                {
                    edit_user: 100004,
                    name: 'SCP巡检环境',
                    time: '2017年11月9日'
                }
            ]
        };
    }
};
</script>
