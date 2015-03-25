package org.arsinfo.rsa;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.Date;
//import java.util.Date;
import java.lang.String;

public class ForceRSA {

	public static RSAKeys generateKeys(int size) {
		BigInteger p = BigInteger.probablePrime( size, new SecureRandom() ); //Nuovo numero primo a 512 bit
		BigInteger q = BigInteger.probablePrime( size, new SecureRandom() ); //Nuovo numero primo a 512 bit
		 
		BigInteger n = p.multiply( q ); // n = p*q
		 
		BigInteger one = BigInteger.ONE;
		 
		BigInteger pMin1 = p.subtract( one ); // p-1
		BigInteger qMin1 = q.subtract( one ); // q-1
		 
		BigInteger fi = pMin1.multiply( qMin1 );
		 
		BigInteger e = p.nextProbablePrime(); //Public
		BigInteger d = e.modInverse( fi ); //Esegue (1/e) % ((p-1)-(q-1))

		RSAKeys keys = new RSAKeys();
		RSAKey publicKey = new RSAKey();
		RSAKey privateKey = new RSAKey();
		
		publicKey.setModulus(n);
		publicKey.setKey(e);
		keys.setPublicKey(publicKey);
		
		privateKey.setModulus(n);
		privateKey.setKey(d);
		keys.setPrivateKey(privateKey);
		
		return keys;
	}
	
	public static BigInteger crypt(BigInteger value, RSAKey publickey) {
		return value.modPow(publickey.getKey(), publickey.getModulus());
	}

	public static BigInteger decrypt(BigInteger crypt, RSAKey privatekey) {
		return crypt.modPow(privatekey.getKey(), privatekey.getModulus());
	}

	public static RSAKey forceRSA(int size, RSAKey publicKey) {
		
		
		BigInteger modulus = publicKey.getModulus();
		BigInteger one = BigInteger.ONE;
		BigInteger six = new BigInteger("6");
		BigInteger thirtysix = new BigInteger("36");

        RSAKey privateKey = new RSAKey();
		privateKey.setModulus(modulus);
		BigInteger p=one.add(one);
		BigInteger q=one.add(one);

		BigSquareRoot app = new BigSquareRoot();
		app.setTraceFlag(false);
        System.out.println ("Computing the square root of modulus");
        int length = modulus.toString ().length ();
        if (length > 20) {
          app.setScale (length / 2);
        }
        BigDecimal sqrt = app.get (modulus);
        System.out.println("End: "+new Date());
        System.out.println ("Iterations " + app.getIterations ());
        System.out.println ("Sqrt " + sqrt.toString ());
        System.out.println (sqrt.multiply (sqrt).toString ());
        System.out.println ("Error " + app.getError ().toString ());
		
//		BigInteger i = new BigInteger(size, new SecureRandom());
        BigInteger i = sqrt.toBigInteger();
        i=i.add(one).divide(six);
		boolean iNotFound=true;


		BigInteger a = one;
		BigInteger c = one;
		BigInteger c1 = one;
		BigInteger c2 = one;
		BigInteger b = one;

		// primo ciclo trovo il min;
		BigInteger max = i;
		int count = 0;
		boolean hasMax=false;
		while(true) {
			count++;
//			System.out.println("max search cycle value i=j="+i);
			
			a = thirtysix.multiply(i.multiply(i)).subtract(six.multiply(i)).subtract(six.multiply(i)).add(one);
			c = thirtysix.multiply(i.multiply(i)).subtract(one);
			b = thirtysix.multiply(i.multiply(i)).add(six.multiply(i)).add(six.multiply(i)).add(one);
			
			//System.out.println("max search cycle value found a="+a+" c="+c +" b="+b);
			
			if (a.equals(modulus)){
				p=six.multiply(i).subtract(one);
				q=p;
				System.out.println("Found a! p="+p);
				System.out.println("Found a! q="+q);
				iNotFound=false;
				break;				 
			} else if (c.equals(modulus)) {
				p=six.multiply(i).add(one);
				q=six.multiply(i).subtract(one);				
				System.out.println("Found c1! p="+p);
				System.out.println("Found c1! q="+q);
				iNotFound=false;
				break;				 				
			} else if (b.equals(modulus)) {
				p=six.multiply(i).add(one);
				q=p;
				System.out.println("Found! p="+p);
				System.out.println("Found! q="+q);
				iNotFound=false;
				break;				 
			} else if (hasMax && modulus.max(a).equals(modulus)) {
				break;
			} else if (modulus.max(a).equals(a)) {
				max=i;
				i=i.subtract(one);
				hasMax=true;
			} else {
				i=i.add(one);
			}
		}

		// ciclo finale a partire da max
		if (iNotFound) {
			System.out.println("Ciclo Max count="+count);
			System.out.println("Found max="+max);
			count=0;
			i=max;
			BigInteger j=i.subtract(one);
			while(true) {
				count++;

				a = thirtysix.multiply(i.multiply(j)).subtract(six.multiply(i)).subtract(six.multiply(j)).add(one);
				c1 = thirtysix.multiply(i.multiply(j)).subtract(six.multiply(i)).add(six.multiply(j)).subtract(one);
				c2 = thirtysix.multiply(i.multiply(j)).add(six.multiply(i)).subtract(six.multiply(j)).subtract(one);
				b = thirtysix.multiply(i.multiply(j)).add(six.multiply(i)).add(six.multiply(j)).add(one);
				
				if (a.equals(modulus)){
					p=six.multiply(i).subtract(one);
					q=six.multiply(j).subtract(one);
					System.out.println("Found a! p="+p);
					System.out.println("Found a! q="+q);
					iNotFound=false;
					break;				 
				} else if (c1.equals(modulus)) {
					p=six.multiply(i).add(one);
					q=six.multiply(j).subtract(one);				
					System.out.println("Found c1! p="+p);
					System.out.println("Found c1! q="+q);
					iNotFound=false;
					break;				 				
				} else if (c2.equals(modulus)) {
					p=six.multiply(i).subtract(one);
					q=six.multiply(j).add(one);
					System.out.println("Found c2 ! p="+p);
					System.out.println("Found c2 ! q="+q);
					iNotFound=false;
					break;				 
				} else if (b.equals(modulus)) {
					p=six.multiply(i).add(one);
					q=six.multiply(j).add(one);
					System.out.println("Found! p="+p);
					System.out.println("Found! q="+q);
					iNotFound=false;
					break;		 
				} else if (modulus.min(b).equals(b)) {
					i=i.add(one);
				} else {
					j=j.subtract(one);
				}
			}
		}

		
		if(!iNotFound) {
			System.out.println("Ciclo principale count="+count);
			BigInteger d = publicKey.getKey().modInverse( p.subtract(one).multiply(q.subtract( one))); //Esegue (1/e) % ((p-1)-(q-1))
			privateKey.setKey(d);
		}
		return privateKey;
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		RSAKeys keys = ForceRSA.generateKeys(32);
		System.out.println("Modulus="+keys.getPublicKey().getModulus());
		System.out.println("PublicKey="+keys.getPublicKey().getKey());
		System.out.println("PrivateKey="+keys.getPrivateKey().getKey());
		
		System.out.println("Start: "+new Date());

		RSAKey privateKey=ForceRSA.forceRSA(30, keys.getPublicKey());
		
		System.out.println("Forced Private Key Found="+privateKey.getKey());
		
	}

}
