import "./Home.css";
import Container from "react-bootstrap/Container";

function Home() {
  return (
    <Container>
      <div className="intro-div">
        <h3>
          Welcome to Aida, an AI driven chatbot who will guide you through a
          design generation and evaluation process
        </h3>
        <div>
          <br></br>

          <p className="intro-text">
            Aida is an AI-driven chatbot designed to evaluate engineering design
            descriptions based on novelty, feasibility, and validity, addressing
            the challenges of efficient and accurate assessment.
          </p>
          <p>
            You will be asked to think, chat and maybe rethink your design
            description until Aida evaluates your idea.
          </p>
        </div>

        {/* <h3>Process flow</h3> */}
        {/* <p className="intro-text">
          The advent of artificial intelligence has revolutionized numerous
          aspects of our lives, transcending various industries and domains.
          Among these, the application of AI in natural language processing
          (NLP) stands out as a transformative force. In the realm of
          engineering design, the evaluation of design descriptions is a crucial
          step that often requires a significant investment of time and
          resources. This research delves into the development of an AI-based
          chatbot tailored to this specific challenge. The motivation behind
          this research stems from the need for efficient and accurate
          evaluation of engineering design descriptions. Traditionally, this
          task has been performed through labor-intensive manual assessments,
          which are not only time-consuming but also prone to subjectivity. The
          emergence of powerful language models, such as BERT base uncased,
          presents an opportunity to automate and enhance this process through
          objective and data-driven means. The primary objective of this
          research is to create an AI-based chatbot that can evaluate design
          descriptions based on three crucial dimensions: novelty, feasibility,
          and validity. By training BERT models on datasets curated from
          engineering design surveys, this chatbot aims to replicate and, in
          certain aspects, surpass human evaluative capabilities. The
          significance of this endeavor lies not only in its potential to
          enhance efficiency but also in the novel approach to evaluation
          itself. This paper proceeds with an exploration of the research's
          background, methodologies, results, and insights. It delves into the
          intricacies of data collection, model fine-tuning, and system
          implementation. Through a detailed analysis of the achieved accuracies
          and the lessons learned, this paper sheds light on the significance of
          data quality, model selection, and architectural innovation in the
          development of AI-driven evaluative systems.
        </p> */}
        {/* <div>
          <ul>
            <li>
             Tell Aida a description of your design.
            </li>
            <li>
              Aida then validates the input. If the input is relevant
              to washing machine engineering design then she proceeds to Novelty
              check.
            </li>
            <li>
              If the validation is successful, then Aida estimates the novelty
              of the idea.
            </li>
            <li>
              If the idea is novel, the model proceeds to check the feasibility
            </li>
            <li>If the idea is feasible, the conversation ends.</li>
          </ul>
        </div> */}
      </div>
    </Container>
  );
}

export default Home;
