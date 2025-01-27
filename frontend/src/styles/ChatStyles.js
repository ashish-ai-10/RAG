import styled from 'styled-components';

export const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 800px;
  margin: auto;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
  padding: 10px;
`;

export const Message = styled.div`
  padding: 10px 15px;
  margin: 5px 0;
  border-radius: 8px;
  max-width: 80%;
  align-self: ${(props) => (props.type === 'user' ? 'flex-end' : 'flex-start')};
  background-color: ${(props) => (props.type === 'user' ? '#0084ff' : '#e0e0e0')};
  color: ${(props) => (props.type === 'user' ? '#fff' : '#333')};
`;

export const InputContainer = styled.div`
  display: flex;
  border-top: 1px solid #e0e0e0;
  padding: 10px;
`;

export const Input = styled.input`
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-right: 10px;
  outline: none;
  font-size: 14px;
`;

export const Button = styled.button`
  padding: 10px 20px;
  background-color: #0084ff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  &:hover {
    background-color: #005bb5;
  }
`;
