"""Ingest pipeline: turns course files into vectors in Pinecone.

A pipeline is described by a JSON manifest (a DAG of operators). Each operator is a plain
function registered in `operators.py`; `runner.py` executes them in dependency order.
"""
