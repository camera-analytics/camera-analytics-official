import React from "react";
import styled from "styled-components";
import logo from "./camera.png";

const Background = styled.div`
  background: ${props => props.c};
  width: 100%;
`;

const Logo = styled.div`
  text-align: center;
  color: ${props => props.c};
  font-size: ${props => props.fs};
  text-transform: ${props => props.tt};
  font-weight: ${props => props.fw};
  display: ${props => props.dis};
  padding-left: 20px;
  &:hover {
    opacity: 0.5;
    transition: all 300ms ease;
  }
`;

const LogoImage = styled.img`
  width: 60px;
  display: inline;
`;

const Container = styled.div`
  padding: 2%;
  text-align: center;
`;

const Header = () => (
  <div>
    <Background c="#fff">
      <Container>
        <LogoImage src={logo} />
        <a href="/">
          <Logo c="#103FB9" fw="800" dis="inline" tt="none" fs="3rem">
            Camlytics
          </Logo>
        </a>
      </Container>
    </Background>
  </div>
);

export default Header;
