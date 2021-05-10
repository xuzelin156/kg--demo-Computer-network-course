# encoding=utf-8
from question_ask.query_main import QAInterface
import streamlit as st

@st.cache(allow_output_mutation=True)
def get_interface():
    interface = QAInterface()
    return interface


qa_interface = get_interface()

st.sidebar.title("问答系统")
st.title('问答系统结果展示')

image = st.sidebar.selectbox('选择你想查看的知识图谱:', ['说明.png','数据链路层.png','计算机网络体系结构.png'])
st.header("1.图谱结果")
st.image(image,use_column_width=True,output_format='PGN')

your_select = st.sidebar.selectbox('demo支持的问题模板',
                                    ['请选择',
                                     '1. 某实体的兄弟关系有哪些',
                                     '2. 某阶段之后是哪个阶段',
                                     '3. 某实体包含了哪些实体',
                                     '4. 与某实体内涵相同的是',
                                     '5. 与某实体内涵相反的是',
                                     '6. 某实体继承自哪个实体',
                                     '7. 某实体参考自哪里/那本教程',
                                     '8. 与某实体可以相互变换的实体有哪些',
                                     '9. 与某实体有因果的实体有哪些？',
                                     '10.某实体的某属性是什么',
                                     '11.某实体是正确的吗？'])
st.header("2.选择的问题")
st.text_area('',your_select)
st.header("3.问题的结果")
question = st.sidebar.text_input("请输入你的问题：")
if question != "":
    st.text_area('',qa_interface.answer(question))


