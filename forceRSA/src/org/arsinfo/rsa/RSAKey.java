package org.arsinfo.rsa;

import java.math.BigInteger;

public class RSAKey {

	BigInteger modulus;
	BigInteger key;
	
	public BigInteger getModulus() {
		return modulus;
	}
	public void setModulus(BigInteger modulus) {
		this.modulus = modulus;
	}
	public BigInteger getKey() {
		return key;
	}
	public void setKey(BigInteger key) {
		this.key = key;
	}
	
}
