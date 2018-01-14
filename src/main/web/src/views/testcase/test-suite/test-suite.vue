<style lang="less">
    @import '../../../styles/common.less';
    @import 'test-suite.less';
</style>


<template>

    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addnewcase" style="margin-top-10">新建套件</i-button>

                <i-button type="success">导入套件</i-button>
            </Col>
        </Row>
        <Row>
            <Col span="8">
                <Card>
                    <p slot="title">
                        <Icon type="ios-copy-outline"></Icon>
                        ERP回归测试套件
                    </p>
                    <div class="height-120px">
                        <Row type="flex" justify="center" align="middle" class="height-100">
                            <Upload action="//jsonplaceholder.typicode.com/posts/">
                                <Button type="ghost" icon="ios-plus-empty">添加用例</Button>
                            </Upload>
                        </Row>
                    </div>
                </Card>
            </Col>
            <Col span="8" class="padding-left-10">
                <Card>
                    <p slot="title">
                        <Icon type="ios-copy-outline"></Icon>
                        校宝秀回归测试套件
                    </p>
                    <div class="height-120px">
                        <Row type="flex" justify="center" align="middle" class="height-100">
                            <Upload multiple action="//jsonplaceholder.typicode.com/posts/">
                                <!--<span>多选文件上传&nbsp;&nbsp;</span>-->
                                <Button type="ghost" icon="ios-plus-empty">添加用例</Button>
                            </Upload>
                        </Row>
                    </div>
                </Card>
            </Col>
            <Col span="8" class="padding-left-10">
                <Card>
                    <p slot="title">
                        <Icon type="ios-copy-outline"></Icon>
                        员工移动端预发布测试套件
                    </p>
                    <div class="height-120px">
                        <Row type="flex" justify="center" align="middle" class="height-100">
                            <Upload
                                action="//jsonplaceholder.typicode.com/posts/"
                                :format="['jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg']"
                                :on-format-error="handleFormatError"
                            >
                                <!--<span>选择图片上传&nbsp;&nbsp;</span>-->
                                <Button type="ghost" icon="ios-plus-empty">添加用例</Button>
                            </Upload>
                        </Row>
                    </div>
                </Card>
            </Col>
        </Row>
        <div class="margin-top-10">
            <Col span="8" class="padding-left-10">
                <Card>
                    <p slot="title">
                        <Icon type="ios-copy-outline"></Icon>
                        校宝家巡检测试套件
                    </p>
                    <div class="height-120px">
                        <Row type="flex" justify="center" align="middle" class="height-100">
                            <Upload
                                action="//jsonplaceholder.typicode.com/posts/"
                                :format="['jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg']"
                                :on-format-error="handleFormatError"
                            >
                                <!--<span>选择图片上传&nbsp;&nbsp;</span>-->
                                <Button type="ghost" icon="ios-plus-empty">添加用例</Button>
                            </Upload>
                        </Row>
                    </div>
                </Card>
            </Col>
            <Col span="8" class="padding-left-10">
                <Card>
                    <p slot="title">
                        <Icon type="ios-copy-outline"></Icon>
                        SCP B端验收测试套件
                    </p>
                    <div class="height-120px">
                        <Row type="flex" justify="center" align="middle" class="height-100">
                            <Upload
                                action="//jsonplaceholder.typicode.com/posts/"
                                :format="['jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg']"
                                :on-format-error="handleFormatError"
                            >
                                <!--<span>选择图片上传&nbsp;&nbsp;</span>-->
                                <Button type="ghost" icon="ios-plus-empty">添加用例</Button>
                            </Upload>
                        </Row>
                    </div>
                </Card>
            </Col>
            <Col span="8" class="padding-left-10">
                <Card>
                    <p slot="title">
                        <Icon type="ios-copy-outline"></Icon>
                        SCP C端回归测试套件
                    </p>
                    <div class="height-120px">
                        <Row type="flex" justify="center" align="middle" class="height-100">
                            <Upload
                                action="//jsonplaceholder.typicode.com/posts/"
                                :format="['jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg']"
                                :on-format-error="handleFormatError"
                            >
                                <!--<span>选择图片上传&nbsp;&nbsp;</span>-->
                                <Button type="ghost" icon="ios-plus-empty">添加用例</Button>
                            </Upload>
                        </Row>
                    </div>
                </Card>
            </Col>
        </div>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'file-upload',
    data () {
        return {
            defaultList: [
                {
                    'name': 'a42bdcc1178e62b4694c830f028db5c0',
                    'url': 'https://o5wwk8baw.qnssl.com/a42bdcc1178e62b4694c830f028db5c0/avatar'
                },
                {
                    'name': 'bc7521e033abdd1e92222d733590f104',
                    'url': 'https://o5wwk8baw.qnssl.com/bc7521e033abdd1e92222d733590f104/avatar'
                }
            ],
            imgName: '',
            visible: false,
            uploadList: []
        };
    },
    methods: {
        handleFormatError (file) {
            this.$Notice.warning({
                title: '文件格式不正确',
                desc: '文件 ' + file.name + ' 格式不正确，请选择图片文件。'
            });
        },
        handleBeforeUpload (file) {
            this.$Notice.warning({
                title: '文件准备上传',
                desc: '文件 ' + file.name + ' 准备上传。'
            });
        },
        handleProgress (event, file) {
            this.$Notice.info({
                title: '文件正在上传',
                desc: '文件 ' + file.name + ' 正在上传。'
            });
        },
        handleSuccess (evnet, file) {
            this.$Notice.success({
                title: '文件上传成功',
                desc: '文件 ' + file.name + ' 上传成功。'
            });
        },
        handleError (event, file) {
            this.$Notice.error({
                title: '文件上传成功',
                desc: '文件 ' + file.name + ' 上传失败。'
            });
        },
        handleView (name) {
            this.imgName = name;
            this.visible = true;
        },
        handleRemove (file) {
            // 从 upload 实例删除数据
            const fileList = this.$refs.upload.fileList;
            this.$refs.upload.fileList.splice(fileList.indexOf(file), 1);
        },
        handleSuccess2 (res, file) {
            // 因为上传过程为实例，这里模拟添加 url
            file.url = 'https://o5wwk8baw.qnssl.com/7eb99afb9d5f317c912f08b5212fd69a/avatar';
            file.name = '7eb99afb9d5f317c912f08b5212fd69a';
        },
        handleFormatError2 (file) {
            this.$Notice.warning({
                title: '文件格式不正确',
                desc: '文件 ' + file.name + ' 格式不正确，请上传 jpg 或 png 格式的图片。'
            });
        },
        handleMaxSize (file) {
            this.$Notice.warning({
                title: '超出文件大小限制',
                desc: '文件 ' + file.name + ' 太大，不能超过 2M。'
            });
        },
        handleBeforeUpload2 () {
            const check = this.uploadList.length < 5;
            if (!check) {
                this.$Notice.warning({
                    title: '最多只能上传 5 张图片。'
                });
            }
            return check;
        },
        addnewcase(){
            axios.get("http://localhost:8090/v1/project",{
                params:{
                    task:"getProjectInfoByName",
                    name:"jessica"
                }
            }).then(function(res){
                console.log(res)
            })
        }
    },
    mounted () {
        this.uploadList = this.$refs.upload.fileList;
    }
};
</script>
